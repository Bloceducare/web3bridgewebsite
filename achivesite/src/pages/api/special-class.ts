import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import specialClassDb from "@server/models/specialClass"
import {  registrationSchema } from "schema";
import { ETrainingsOptions, PaymentStatus, Tracks } from "enums";
import validate from "@server/validate";
import { sendSms } from "@server/sms";
import { sendEmail } from "@server/mailer";
import reportError from "@server/services/report-error";
import useVoucher from "@server/voucher";
import {COHORT_REGISTRATION_OPENED} from "config/constant"


const router = createRouter<NextApiRequest, NextApiResponse>();


const userMax ={
  0:50, // 20
  1:50, // 20
  2:50, // 20
  3:50, //10
  4:50 //10
}

router.get(async (req: NextApiRequest, res: NextApiResponse)=>{
  const p = req.query.type
  const findType = ETrainingsOptions[+p-1]
  
  try{

    const user = await specialClassDb.find({
      AreaOfInterest:findType
    }) 
    
    return res.status(200).json({
      left:userMax[+p-1] - user.length,
      isCompleted:userMax[+p-1] == user.length,
      })

  }
  catch(e){
    return res.status(500).json({
      message:e
      })
  }
  

})
.use(async (req, res, next) => {
  // this serve as the error handling middleware
 let  schema =registrationSchema.specialClass  
  await validate(schema)(req, res, next)
})

// create a user
.post(async (req: NextApiRequest, res: NextApiResponse) => {
 if(!COHORT_REGISTRATION_OPENED){
return res.status(423).json({
      message: "registration closed",
      status: false,
    });
}
  let userDb = specialClassDb;
 


  if(Object.values(Tracks).indexOf(req.body.currentTrack) === -1){
    return res
    .status(400)
    .send({ status: false, error: "Invalid track" });
  }
  const { email, phone, currentTrack,name } = req.body;

 
  try {
    await connectDB();

    const userExists= await specialClassDb.findOne({ email });

    if(userExists?.paymentStatus ===PaymentStatus.success){
      await closeDB();
      return res
        .status(423)
        .json({ status: false, error: `This user already exists  ` , paymentStatus:userExists.paymentStatus ?? PaymentStatus.pending });
    }


    if (userExists) {
      await closeDB();
      return res
        .status(423)
        .json({ status: false, error: "This user already exists" });
    }   

    //   await Promise.all([
    //     sendSms({recipients:phone}), 
    //     sendEmail({email, name, type:currentTrack,file:"webemail" })
    // ])
 
    

  
 
    
    const userData: any = new userDb({
      ...req.body,
      paymentStatus:PaymentStatus.pending,   
    
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
})



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
  let userDb= specialClassDb  

  const { currentTrack, page }: IQuery = req.query;

  try {


  const re =  await  userDb.find({})
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
