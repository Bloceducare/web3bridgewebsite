import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3UserDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import specialClassDb from "@server/models/specialClass";
import { sendEmail } from "@server/mailer";
import {PaymentStatus, Tracks} from "enums"
import Paystack from "paystack"
import { verifyPaymentSchema } from 'schema';
import {ISmsData} from "types"
import { sendSms } from "@server/sms";
import validate from "@server/validate";
import reportError from "@server/services/report-error";

const userEmail = {
  web2:"web2",
  web3:"web3",
  specialClass: {
    1:"webemail",
    2:"webemail",
    3:"webemail",
    4:"webemail",
    5:"webemail"
  }
}
const router = createRouter<NextApiRequest, NextApiResponse>();
const paystack = Paystack(process.env.PAYMENT_SECRET);

router
// .use(async (req, res, next) => {
//   await validate(verifyPaymentSchema)(req, res, next)
// }
// )
// verify payment
.post(async (req: NextApiRequest, res: NextApiResponse) => {
    const getTrack = (trackUrl:string) => {
      if(!trackUrl) return [0, 0]
      const tr = trackUrl?.split('/')?.pop()?.split("?") ?? []
      const [track, type] = tr
      let sortType;
      if(type){
        sortType =  type.split("").slice(-1)
      }
        return [track, sortType?.[0]]
    }
    let userDb;

    if(!req?.body?.data?.customer?.email || !req?.body?.data?.reference){
      return res.status(423).json({
        status:false,
        message:"not data sent",
        data:req.body
      })
    }
    const { reference,customer:{email=""}={}, metadata:{referrer} } = req.body.data;

 


   
    const [track, sortType] = getTrack(referrer)
  
    await connectDB();
    if(track===Tracks.web2){
        userDb = web2UserDb
       
    }

    if(track ===Tracks.web3){
      userDb = web3UserDb 
    }
    if(track ===Tracks.specialClass){
      userDb = specialClassDb
    }
    
    
    
    
  try {

  
  // verify payment status
 

   const data = await  paystack.transaction.verify(reference)
   if(!userDb) return res.status(404).json({
     status:false,
     message:"payment not found"
   })
  //  console.log(data?.data?.status,"Data?????>>>>>")
    if(data?.data?.status !== "success"){
      return res.status(423).json({
        status: false,
        message: "payment not valid",
      });
    }

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

    if(!userDetails.currentTrack){
      await closeDB();
        return res.status(404).json({
            status: false,
            message: "track not found"
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
       const [,sms={balance:""} as ISmsData] =  await Promise.all<any>([
        userDb.updateOne({email}, {
            $set: {paymentStatus: PaymentStatus.success}
        }),
       
   sendSms({recipients:userDetails.phone}), 
    sendEmail({email, name:userDetails.name, type:userDetails.currentTrack, 
      file:userDetails.currentTrack =="specialClass" ? userEmail?.[userDetails?.currentTrack]?.[sortType] :userEmail?.[userDetails?.currentTrack],      
  }),
      ])


      if(++sms.balance <= 100 ){
        sendSms({recipients:["2348130192777"], message:`low balance, ${++sms.balance-2} sms balance left`})
      }


      await closeDB()

        return res.status(201).json({ message: "payment verified", status: true });


  } catch (e) {
    // reportError

    reportError(`error occurred at ${__filename}\n environment:${process.env.NODE_ENV}\n ${e} `)
    console.log(e,'error caused wss')

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
