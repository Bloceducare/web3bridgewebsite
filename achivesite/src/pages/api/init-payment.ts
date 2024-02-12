import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import userDb from "@server/models/cohortUsers";
import { sendEmail } from "@server/mailer";
import {PaymentStatus} from "enums"
import { initPaymentSchema,  } from 'schema';
import validate from "@server/validate";

const router = createRouter<NextApiRequest, NextApiResponse>();

router.use(async (req, res, next) => {
  await validate(initPaymentSchema)(req, res, next)
}
)
// init payment
.post(async (req: NextApiRequest, res: NextApiResponse) => {
  await connectDB();
  const { reference, email, paymentMethod} = req.body;
  try {
    // user details
    const userDetails = await userDb.findOne({ email });
   // check if user exists
    if(!userDetails){
        return res.status(404).json({
            status: false,
            message: "user not found"
        })
    }

    if(userDetails.paymentMethod === paymentMethod){
        return res.status(423).json({
            status: false,
            message:"payment method do not match"
        })
    }
    // check if payment is already successful
    if(userDetails.paymentStatus === PaymentStatus.success){
        return res.status(423).json({
            status: true,
            message: "payment already verified"
        })
    }

        // update user payment status
      await userDb.updateOne({email}, {
        $set: {
            paymentStatus: PaymentStatus.pending,
            paymentReference: reference
        }
    })
      await closeDB()
        return res.status(201).json({ message: "payment verified", status: true });
  } catch (e) {
    console.log(e,'error caused')
    return res.status(500).json({
      status: false,
      error: e,
      message:"Internal server error "
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
