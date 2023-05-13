import type { NextApiRequest, NextApiResponse } from "next";
import { createRouter } from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3UserDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import specialClassDb from "@server/models/specialClass";
import { sendEmail } from "@server/mailer";
import { PaymentStatus, Tracks } from "enums";
import { verifyPaymentSchema } from "schema";
import { ISmsData } from "types";
import { sendSms } from "@server/sms";
import validate from "@server/validate";
import { userEmail, webPayment } from "@server/config";
import reportError from "@server/services/report-error";

const router = createRouter<NextApiRequest, NextApiResponse>();

const PaymentPck = require("flutterwave-node-v3");
const pyt = new PaymentPck(
  process.env.FLW_PUBLIC_KEY,
  process.env.FLW_SECRET_KEY
);

router
  // .use(async (req, res, next) => {
  //   await validate(verifyPaymentSchema)(req, res, next)
  // }
  // )
  // verify payment
  .post(async (req: NextApiRequest, res: NextApiResponse) => {
    if (!req?.body?.customer?.email || !req?.body?.id) {
      return res.status(425).json({
        status: false,
        message: "not data sent",
        data: req.body,
      });
    }

    const { customer: { email = "" } = {} } = req.body;

    await connectDB();

    const secretHash = process.env.PYT_SECRET_HASH;
    const signature = req.headers["verif-hash"];
    if (!signature || signature !== secretHash) {
      res.status(401).json({});
    }

    try {
      const payload = req.body;
      // verify payment status
      const result = await pyt.Transaction.verify({ id: String(payload.id) });

      let tracks = {
        web2: web2UserDb,
        web3: web3UserDb,
        specialClass: specialClassDb,
      };

      const track = result.data.meta.track;

      const userDb = tracks[track];

      if (!userDb)
        return res.status(404).json({
          status: false,
          message: "track not found",
        });

      // user details
      const userDetails = await userDb.findOne({ email });

      // check if user exists
      if (!userDetails?._id) {
        await closeDB();
        return res.status(404).json({
          status: false,
          message: "user not found",
        });
      }

      if (!userDetails.currentTrack) {
        await closeDB();
        return res.status(404).json({
          status: false,
          message: "track not found",
        });
      }

      // check if payment is already successful
      if (userDetails.paymentStatus === PaymentStatus.success) {
        return res.status(423).json({
          status: true,
          message: "payment already verified",
        });
      }

      let expectedAmount = 0;
      const expectedCurrency = "NGN";

      if (track === Tracks.web2 || track === Tracks.web3) {
        expectedAmount = webPayment.naira;
      }

      if (expectedAmount === 0) {
        res.status(429).json({
          message: "amount can not be zero",
        });
      }

      if (
        result.data.status === "successful" &&
        result.data.amount >= expectedAmount &&
        result.data.currency === expectedCurrency
      ) {
        // Success! Confirm the customer's payment
        // update user payment status
        const [, sms = { balance: "" } as ISmsData] = await Promise.all<any>([
          userDb.updateOne(
            { email },
            {
              $set: { paymentStatus: PaymentStatus.success },
            }
          ),

          sendSms({ recipients: userDetails.phone }),
          sendEmail({
            email,
            name: userDetails.name,
            type: userDetails.currentTrack,
            currentTrack: userDetails.currentTrack,
            file: userEmail?.[userDetails?.currentTrack],
            userDb,
          }),
        ]);

        if (+sms.balance <= 100) {
          sendSms({
            recipients: "+2348130192777",
            message: `low balance, ${++sms.balance - 2} sms balance left`,
          });
        }

        await closeDB();

        return res
          .status(201)
          .json({ message: "payment verified", status: true });
      }

      return res.status(429).json({
        status: true,
        message: "Payment not valid",
      });
    } catch (e) {
      // reportError
      reportError(
        `error occurred at ${__filename}\n environment:${process.env.NODE_ENV}\n ${e} `
      );
      console.log(e, "error caused wss");

      return res.status(500).json({
        status: false,
        error: e,
        message: "Internal server error ",
      });
    }
  });

export default router.handler({
  // @ts-ignore
  onError: (err, req, res, next) => {
    console.error(err.stack);
    res.status(500).end("Something broke!");
  },
  onNoMatch: (req, res) => {
    res.status(404).end("Page is not found");
  },
});
