import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3UserDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import specialClassDb from "@server/models/specialClass"
import { sendEmail } from "@server/mailer";
import {PaymentStatus, Tracks} from "enums"
import { verifyPaymentSchema } from 'schema';
import {ISmsData} from "types"
import { sendSms } from "@server/sms";
import validate from "@server/validate";
import {webPayment, specialClassPayment} from "@server/config"
import LazerPay from "lazerpay-node-sdk";
import reportError from "@server/services/report-error";
import {userEmail} from "@server/config"


const router = createRouter<NextApiRequest, NextApiResponse>();

const lazerpay = new LazerPay(process.env.LAZERPAY_PUBLIC_KEY as string, process.env.LAZERPAY_SECRET_KEY as string);

router

// verify payment
.post(async (req: NextApiRequest, res: NextApiResponse) => {
    const {reference, amountReceived, status, metadata:{track="", trackType="", trackNumber=0}={}, customer:{email=''}={}, feeInCrypto } = req.body
    let userDb;

    let payment;
    if(Tracks.specialClass == track){
       payment = specialClassPayment[trackType]
    }
  if(!track){
    return res.status(404).json({
      status: false,
      message: "track not found"
    })
  }

  if(!email){
    return res.status(423).json({
      status: false,
      message: "email not found"
    })
  }
  
  if((amountReceived - feeInCrypto) !== payment.USD){
    return res.status(423).json({
      status: false,
      message: `Amount received is not valid, expected ${payment.USD}`,
    })
  }

  if(status !== "confirmed"){
   
    return res.status(423).json({
      status: false,
      message: "payment not valid",
    })
  }

await connectDB();

if(track ===Tracks.specialClass){
  userDb = specialClassDb
  
}
if(track===Tracks.web2){
    userDb = web2UserDb
    
}

if(track===Tracks.web3){
    userDb = web3UserDb
}
      try{
  // user details
const userDetails = await userDb.findOne({ email });
// check if user exists
if(!userDetails){
  await closeDB();
    return res.status(404).json({
        status: false,
        message: "user not found"
    })
}

// check if payment is already successful
if(userDetails.paymentStatus === PaymentStatus.success){
  await closeDB();
    return res.status(423).json({
        status: false,
        message: "payment already successful"
    })
}

// verify payment
const payload = {
  identifier: reference,
};
const {data} = await lazerpay.Payment.confirmPayment(payload);

if(data.status !== "confirmed" || ((amountReceived - feeInCrypto) !== payment.USD)){
  await closeDB();
  return res.status(400).json({
    status: false,
    message: "payment not valid",
  })
}

// update payment status

      // update user payment status
        const [,sms={balance:""} as ISmsData] =  await Promise.all<any>([
          userDb.updateOne({email}, {
              $set: {paymentStatus: PaymentStatus.success}
          }),
         
      sendSms({recipients:userDetails.phone}),
    sendEmail({email, 
      name:userDetails.name, 
      type:userDetails.currentTrack, 
      currentTrack:userDetails.currentTrack,
      file:userDetails.currentTrack =="specialClass" ? userEmail?.[userDetails?.currentTrack]?.[trackNumber] :userEmail?.[userDetails?.currentTrack],      
  })
        ])
     
        if(+sms?.balance <= 100 ){
          sendSms({recipients:["2348130192777"], message:`low balance, ${++sms.balance-2} sms balance left`})
        }

        await closeDB();
   return res.status(200).json({
        status: true,
        message: "payment successful",
        data:req.body
   })

      }
      catch(error){
        reportError(`error occurred at ${__filename}\n environment:${process.env.NODE_ENV}\n ${error} `)
    
        console.log('error lazer', error)
        return res.status(500).json({
          status: false,
          message: "Server Error",
        })
      }

});



export default router.handler({
  // @ts-ignore
  onError: (err, req, res, next) => {
    console.log("something went wrong", err);
    res.status(500).end("Something broke!");
  },
  onNoMatch: (req, res) => {
    res.status(404).end("Page is not found");
  },
});
