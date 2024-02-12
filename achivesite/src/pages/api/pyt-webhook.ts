import type { NextApiRequest, NextApiResponse } from "next";
import { createRouter } from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3UserDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import specialClassDb from "@server/models/specialClass";
import { sendEmail } from "@server/mailer";
import { EspecializedOptions, PaymentStatus, Tracks } from "enums";
import { verifyPaymentSchema } from "schema";
import { ISmsData } from "types";
import { sendSms } from "@server/sms";
import validate from "@server/validate";
import { isDev, specialClassPayment, userEmail, webPayment } from "@server/config";
import reportError from "@server/services/report-error";

const router = createRouter<NextApiRequest, NextApiResponse>();

const PaymentPck = require("flutterwave-node-v3");
const pyt = new PaymentPck(
  process.env.FLW_PUBLIC_KEY,
  process.env.FLW_SECRET_KEY
);

router.post(async (req: NextApiRequest, res: NextApiResponse) => {
  req.body = isDev ? req.body : req.body.data;
  const sentData = req?.body?.customer?.email;
  const sentId = req?.body?.id;

  if (!sentData || !sentId) {
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
    return res.status(401).json({
      error: "hash not math",
    });
  }

  try {
    const payload = req.body;
    // verify payment status
    const result = await pyt.Transaction.verify({
      id: String(payload.id),
    });

    let tracks = {
      web2: web2UserDb,
      web3: web3UserDb,
      specialClass: specialClassDb,
    };

    const track = result?.data?.meta?.track;
    const AOI = result?.data?.meta?.AOI // Area of Interest
    const userDb = tracks[track];

    if(!AOI){
      return res.status(400).json({error:"Area of interest is required"})
    }

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
    let expectedCurrency = Boolean(result?.data?.meta?.isNaira) ? "NGN" : "USD";

    if (track === Tracks.web2 || track === Tracks.web3) {
      expectedCurrency ="NGN"
      expectedAmount = webPayment.naira;    
    }

 
    if(track===Tracks.specialClass){
      if(Boolean(result?.data?.meta?.isNaira)){
        expectedAmount = specialClassPayment[AOI]?.naira 

        
      } else {
        expectedAmount = specialClassPayment[AOI]?.USD
      }
    }

    if (expectedAmount === 0) {
      return res.status(422).json({
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

        // sendSms({ recipients: userDetails.phone }),
        sendEmail({
          email,
          name: userDetails.name,
          type: userDetails.currentTrack,
          currentTrack: userDetails.currentTrack,
          file: userDetails?.currentTrack==Tracks.specialClass ? "webemail":userEmail?.[userDetails?.currentTrack],
          userDb,
        }),
      ]);

      // if (+sms.balance <= 100) {
      //   sendSms({
      //     recipients: "+2348130192777",
      //     message: `low balance, ${++sms.balance - 2} sms balance left`,
      //   });
      // }
      await closeDB();
      return res
        .status(201)
        .json({ message: "payment verified", status: true });
    } else {
      return res.status(429).json({
        status: true,
        message: "Payment not valid",
      });
    }
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
