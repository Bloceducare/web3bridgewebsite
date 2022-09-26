import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3UserDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import {PaymentStatus} from "enums"
import Paystack from "paystack"
import { verifyPaymentSchema } from 'schema';
import validate from "@server/validate";

const router = createRouter<NextApiRequest, NextApiResponse>();
const paystack = Paystack(process.env.PAYMENT_SECRET);


router.use(async (req, res, next) => {
  await validate(verifyPaymentSchema)(req, res, next)
}
)
// verify payment
.post(async (req: NextApiRequest, res: NextApiResponse) => {
  let userDb;
  await connectDB();
  
  const { reference, email, currentTrack} = req.body;
  if(currentTrack === 'web2'){
    userDb = web2UserDb
  } else {
    userDb = web3UserDb
  }



  try {
  // verify payment status
   const data = await  paystack.transaction.verify(reference)
   
   
    if(data?.data?.status !== 'success'){
      await closeDB()
      return res.status(423).json({
        status: false,
        message: "payment not valid",
      });
    }


    // user details
    const userDetails = await userDb.findOne({ email });
   // check if user exists
    if(!userDetails){
      await closeDB()
        return res.status(404).json({
            status: false,
            message: "user not found"
        })
    }
    // check if payment is already successful
    if(userDetails.paymentStatus === PaymentStatus.success){
      await closeDB()
        return res.status(423).json({
            status: true,
            message: "payment already verified"
        })
    }

      await closeDB()
    
    if(data?.data?.status === 'success'){
      return res.status(201).json({ message: "payment verified", status: true });
    }
    return res.status(423).json({
        status: false,
        message: "We're currently unable to verify your payment, please reload your page" ,
    })
  } catch (e) {
    console.log(e,'error caused verify payment')
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
