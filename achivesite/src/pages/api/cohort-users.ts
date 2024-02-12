import type { NextApiRequest, NextApiResponse } from "next";
import { createRouter } from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3userDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import cartesiUserDb from "@server/models/cartesi";
import zkclassUserDb from "@server/models/zkclass";
import { registrationSchema } from "schema";
import { PaymentMethod, PaymentStatus, Tracks } from "enums";
import validate from "@server/validate";
import reportError from "@server/services/report-error";
import {
  COHORT_REGISTRATION_OPENED,
  registrationPaused,
  TRAINING_CLOSED,
} from "config/constant";
import { sendSms } from "@server/sms";
import { sendEmail } from "@server/mailer";

const router = createRouter<NextApiRequest, NextApiResponse>();

router.get(async (req, res) => {
  const dbs = {
    web2: web2UserDb,
    web3: web3userDb,
    cartesi: cartesiUserDb,
    zkclass: zkclassUserDb,
  };

  const { currentTrack, page, email }: IQuery = req.query;
  // @ts-ignore
  const userDb = dbs[currentTrack];
  if (!userDb) {
    return res.status(404).json({
      message: "user track not found",
      error: "user track not found",
    });
  }

  await connectDB();

  try {
    const data = email
      ? await userDb.findOne({ email })
      : await userDb.find({ paymentStatus: "success" });

    closeDB();
    return res.status(200).json({
      status: true,
      data,
    });

    // return res.status(200).json({
    //   status: true,
    // });
  } catch (e) {
    reportError;
    return res.status(500).json({
      status: false,
      error: "server error" + e,
    });
  }
});

router
  .use(async (req, res, next) => {
    console.log('request..',req.body)
    let schema;
    if (req.body.currentTrack || req.query.currentTrack) {
      schema =
        registrationSchema[req.body.currentTrack ?? req.query.currentTrack];
    } else {
      throw new Error("Error Occurred");
    }
    await validate(schema)(req, res, next);
  })

  // create a user
  .post(async (req: NextApiRequest, res: NextApiResponse) => {
    if (registrationPaused) {
      return res.status(423).json({
        message: "Registration paused , Please check back later",
        status: false,
      });
    }
    if (TRAINING_CLOSED[req.body.currentTrack]) {
      console.log('error encounterred')
      return res.status(423).json({
        message: "registration closed",
        status: false,
      });
    }

    const dbs = {
      web2: web2UserDb,
      web3: web3userDb,
      cartesi: cartesiUserDb,
      zkclass: zkclassUserDb,
    };
    const userDb = dbs[req.body.currentTrack];

    if (!userDb) {
      return res
        .status(400)
        .send({ status: false, error: "Invalid track supplied" });
    }

    if (Object.values(Tracks).indexOf(req.body.currentTrack) === -1) {
      return res.status(400).send({ status: false, error: "Invalid track" });
    }

    const { email, phone, currentTrack, name } = req.body;

    try {
      await connectDB();
      console.log('db connected successfully');

      const userExists = await userDb.findOne({ email });
      
      if (userExists) {
        
        await closeDB();
        return res.status(423).send({
          status: false,
          error: "This user already exists",
          pyt: userExists._doc.paymentStatus,
          pytMethod: userExists._doc.paymentMethod,
        });
      }

      const smsMessage = req.body.currentTrack == "cartesi" && {
        message:
          "Welcome to Web3Bridge Cartesi Masterclass Training. Do check your mail for further information",
      };

      await Promise.all([
        sendSms({ recipients: phone, ...smsMessage }),
        sendEmail({
          email,
          name,
          type: currentTrack,
          file: req.body.currentTrack,
          currentTrack: req.body.currentTrack,
          userDb:req.body.currentTrack
        }),
      ]);

      const userData: any = new userDb({
        ...req.body,
      });

      console.log('data:::', userData);
      const { _doc } = await userData.save();

      await closeDB();

      return res.status(201).json({
        message:
          "Registration successful! Please check your email for further instructions",
        ..._doc,
      });
    } catch (e) {
      
      reportError(
        `error occurred at ${__filename}\n environment:${process.env.NODE_ENV}\n ${e} `
      );

      
      return res.status(423).json({
        error: e,
        status: false,
      });
    }
  });

interface IQuery {
  currentTrack?: string | string[] | undefined;
  page?: number | string;
  email?: string;
  status?: string;
}

export default router.handler({
  // @ts-ignore
  onError: (err, req, res, next) => {
    console.error(err.stack);
    reportError(err);
    res.status(500).end("Something broke!");
  },
  onNoMatch: (req, res) => {
    res.status(404).end("Page is not found");
  },
});
