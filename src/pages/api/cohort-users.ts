import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3userDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import cairoUserDb from "@server/models/cairo";
import {  registrationSchema } from "schema";
import { PaymentStatus, Tracks } from "enums";
import validate from "@server/validate";
import { sendSms } from "@server/sms";
import { sendEmail } from "@server/mailer";
import reportError from "@server/services/report-error";
import useVoucher from "@server/voucher";
import {COHORT_REGISTRATION_OPENED, TRAINING_CLOSED} from "config/constant"


const router = createRouter<NextApiRequest, NextApiResponse>();

router
.use(async (req, res, next) => {
  let schema;
  if(req.body.currentTrack || req.query.currentTrack){
    schema =registrationSchema[req.body.currentTrack ?? req.query.currentTrack]
  }
 
  else {
  throw new Error("Error Occurred")
  }
  await validate(schema)(req, res, next)
})

// create a user
.post(async (req: NextApiRequest, res: NextApiResponse) => {
  
 if(TRAINING_CLOSED[req.body.currentTrack]){
return res.status(423).json({
      message: "registration closed",
      status: false,
    });
}
  let userDb;
  if(req.body.currentTrack === "web2"){
    userDb = web2UserDb
  }

  if(req.body.currentTrack === "web3"){
    userDb = web3userDb
  }
  if(req.body.currentTrack === "cairo"){
    userDb = cairoUserDb
  }

  if(Object.values(Tracks).indexOf(req.body.currentTrack) === -1){
    return res
    .status(400)
    .send({ status: false, error: "Invalid track" });
  }
  const { email, phone, currentTrack,name,voucher } = req.body;

  const applyVoucher = req.body.currentTrack  !=='cairo'
  if(applyVoucher && !voucher){
    await closeDB;
    return res.status(423).json({
     error:'voucher is required',
     status:false
    })
  }


  try {
    await connectDB();

    const userExists= await userDb.findOne({ email });


    if (userExists) {
      await closeDB();
      return res
        .status(423)
        .send({ status: false, error: "This user already exists" });
    }
    

    if( !!voucher){
      const  userVoucher = await useVoucher({identifier: voucher, email})

      if(!userVoucher.status){
        await closeDB;
        return res.status(userVoucher.code ?? 400).json({
          ...userVoucher
        })
      }  
    }
const smsMessage = (req.body.currentTrack  =='cairo' && {message:"Welcome to Web3Bridge Cairo Training. Do check your mail for further information"})

     await Promise.all([sendSms({recipients:phone,...smsMessage}), 
      sendEmail({email, name, type:currentTrack, file:req.body.currentTrack,
        currentTrack:req.body.currentTrack
    })])

  
 
    
    const userData: any = new userDb({
      ...req.body,   
    
    }, 
);

    const { _doc } = await userData.save();

    await closeDB();

    return res.status(201).json({ message: "Registration was successful, please check your email for further instructions" , ..._doc });
  } catch (e) {

    reportError(`error occurred at ${__filename}\n environment:${process.env.NODE_ENV}\n ${e} `)
  
    console.log("Error occuredd", e);
    return res.status(423).json({
      error: e,
      status: false,
    });
  }
});

interface IQuery {
  currentTrack?: string | string[] | undefined;
  page?: number | string;
}

router
// .get(async (req, res) => {
//   let userDb;
//   if(req.query.currentTrack === "web2"){
//     userDb = web2UserDb
//   }

//   if(req.query.currentTrack === "web3"){
//     userDb = web3userDb
//   }
  
//   const { currentTrack }: IQuery = req.query;

//   try {
//     const data = await web3userDb.find({})
//     console.log(data, currentTrack)
//     return res.status(200).json({
//       status: true,
//       message:data
//     })
//   } catch (e) {
//     return res.status(500).json({
//       status: false,
//       error: "server error",
//     });
//   }
// })
.get(async (req, res) => {
  let userDb;

    if(req.query.currentTrack === "web2"){
    userDb = web2UserDb
  }

  if(req.query.currentTrack === "web3"){
    userDb = web3userDb
  }
  if(req.query.currentTrack === "cairo"){
    userDb =cairoUserDb
  }
  

  const { currentTrack, page }: IQuery = req.query;

  try {
    // const users = await web3userDb.find({
    //   email:'okel@'
    //   // ...(!!currentTrack && { currentTrack }),
    // });

  const re =  await  web2UserDb.find({})
console.log(web2UserDb, web3userDb, re)
    return res.status(200).json({
      status: true,
      data:' users',
    });
  } catch (e) {
    reportError
    return res.status(500).json({
      status: false,
      error: "server error" + e,
    });
  }
});

export default router.handler({
  // @ts-ignore
  onError: (err, req, res, next) => {
    console.error(err.stack);
    reportError(err)
    res.status(500).end("Something broke!");
  },
  onNoMatch: (req, res) => {
    res.status(404).end("Page is not found");
  },
});