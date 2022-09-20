import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3UserDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import { sendEmail } from "@server/mailer";
import {PaymentStatus, Tracks} from "enums"
import Paystack from "paystack"
import { verifyPaymentSchema } from 'schema';
import {ISmsData} from "types"
import { sendSms } from "@server/sms";
import validate from "@server/validate";

const router = createRouter<NextApiRequest, NextApiResponse>();
// const paystack = Paystack(process.env.PAYMENT_SECRET);

router

// verify payment
.post(async (req: NextApiRequest, res: NextApiResponse) => {
    // const getTrack = (track:string) => track.split('/').pop()
    console.log(req.body.data, 'req.body.data')

   return res.status(200).json({
        status: true,
        message: "payment successful",
        data:req.body.data
   })

//     const track = getTrack(referrer)
//     if(track===Tracks.web2){
//         userDb = web2UserDb
       
//     } else {
//         userDb = web3UserDb
//     }
    
    
//   await connectDB();
//   try {
//   // verify payment status
//    const data = await  paystack.transaction.verify(reference)
//     if(data.status === false){
//       return res.status(423).json({
//         status: false,
//         message: "payment not valid",
//       });
//     }

//     // user details
//     const userDetails = await userDb.findOne({ email });
//    // check if user exists
//     if(!userDetails){
//         return res.status(404).json({
//             status: false,
//             message: "user not found"
//         })
//     }
//     console.log(userDetails.phone, userDetails.name, track, 'suer details', userDetails)

//     // check if payment is already successful
//     if(userDetails.paymentStatus === PaymentStatus.success){
//         return res.status(423).json({
//             status: true,
//             message: "payment already verified"
//         })
//     }
//         console.log("paysacj data", data)
    
//         // update user payment status
//        const [,sms={balance:""} as ISmsData] =  await Promise.all<any>([
//         userDb.updateOne({email}, {
//             $set: {paymentStatus: PaymentStatus.success}
//         }),
//         // send email
//        sendSms({recipients:userDetails.phone}),  // send text message
//        sendEmail({email, name:userDetails.name, currentTrack:track, file:"registration"}),
//     //    sendEmail({email, currentTrack, name, file:"registration", }),
//     //    sendSms({recipients:phone})
//       ])

//     //   if(++sms.balance <= 100 ){
//     //     sendSms({recipients:["2348130192777"], message:`low balance, ${++sms.balance-2} sms balance left`})
//     //   }


//       await closeDB()

//         return res.status(201).json({ message: "payment verified", status: true });
    

//     // return res.status(423).json({
//     //     status: false,
//     //     message: "Payment verification failed",
//     // })


//   } catch (e) {
//     console.log(e,'error caused')
//     return res.status(500).json({
//       status: false,
//       error: e,
//       message:"Internal server error "
//     });
//   }
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
