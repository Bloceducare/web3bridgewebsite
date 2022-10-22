import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3userDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import { PaymentStatus, Tracks } from "enums";
import reportError from "@server/services/report-error";

const router = createRouter<NextApiRequest, NextApiResponse>();

router
.use(async(req,res,next)=>{
  await connectDB()

  const { currentTrack, email }= req.query;

  if(!currentTrack || !(Object.values(Tracks).some(i=>i===currentTrack))) {
      await closeDB()
    return res.status(404).json({status:false, message:'invalid track'})
  }


  if(!email) {
    await closeDB()
  return res.status(404).json({status:false, message:'supply an email'})
}





  return next()
})


// user
.get(async(req,res)=>{

  const { email, currentTrack } = req.query;
  let userDb;

  if(currentTrack === "web2"){
    userDb = web2UserDb
  }

  if(currentTrack === "web3"){
    userDb = web3userDb
  }

  try {

    const user = await  userDb.findOne({email})

    await closeDB()
    return res.status(200).json({
      status: true,
          message: user,
       })

  }

  catch(e){

  }

})






export default router.handler({
  // @ts-ignore
  onError: (err, req, res, next) => {
    console.error(err.stack);
    reportError(err)
    res.status(500).end("Something broke!");
  },
  onNoMatch: (req, res) => {
    res.status(404).end("Page is not found info");
  },
});
