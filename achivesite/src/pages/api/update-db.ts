import type { NextApiRequest, NextApiResponse } from "next";
import { createRouter } from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3UserDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import { PaymentStatus } from "enums";
import validate from "@server/validate";
import { ISmsData } from "types";
import { sendSms } from "@server/sms";
import { sendEmail } from "@server/mailer";

const router = createRouter<NextApiRequest, NextApiResponse>();

router.post(async (req: NextApiRequest, res: NextApiResponse) => {
  const { email } = req.body;
  if (!email) {
    return res.status(400).json({
      status: false,
      message: "provide email",
    });
  }
  let userDb;
  await connectDB();
  userDb = web3UserDb;
  // userDb = web2UserDb

  try {
    // user details
    const userDetails = await userDb.findOne({ email });
    // check if user exists
    if (!userDetails) {
      return res.status(404).json({
        status: false,
        message: "user not found",
      });
    }

    if (userDetails.paymentStatus === PaymentStatus.success) {
      return res.status(200).json({
        status: false,
        message: "payment already successful",
      });
    }

    //       // update user payment status
    // const [, sms = { balance: "" } as ISmsData] = await Promise.all<any>([
    //   userDb.updateOne(
    //     { email },
    //     {
    //       $set: { paymentStatus: PaymentStatus.success },
    //     }
    //   ),

    //   // sendSms({recipients:userDetails.phone}),
    //   sendEmail({
    //     email,
    //     name: userDetails.name,
    //     type: userDetails.currentTrack,
    //     currentTrack: userDetails.currentTrack,
    //     file: "web3",
    //     userDb,
    //   }),
    // ]);

    // sendEmail({
    //   email,
    //   name: userDetails.name,
    //   type: userDetails.currentTrack,
    //   currentTrack: userDetails.currentTrack,
    //   file: userEmail?.[userDetails?.currentTrack],
    //   userDb,
    // }),

    await closeDB();

    return res.status(201).json({
      status: true,
      message: "success",
    });
  } catch (e) {
    console.log(e, "error caused");
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
