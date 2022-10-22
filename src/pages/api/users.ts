import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3userDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import { PaymentStatus, Tracks } from "enums";
import reportError from "@server/services/report-error";

const router = createRouter<NextApiRequest, NextApiResponse>();


interface IQuery {
  currentTrack?: Tracks | undefined;
  page?: number | string;
  paymentStatus?: PaymentStatus
}

router
.use(async(req,res,next)=>{
  await connectDB()

  const { currentTrack }: IQuery = req.query;

  if(!currentTrack || !(Object.values(Tracks).some(i=>i===currentTrack))) {
      await closeDB()
    return res.status(404).json({status:false, message:'invalid track'})
  }



  return next()
})

.get(async (req, res) => {

  let userDb;
  const { currentTrack, paymentStatus }: IQuery = req.query;

  if(currentTrack === "web2"){
    userDb = web2UserDb
  }

  if(currentTrack === "web3"){
    userDb = web3userDb
  }


    
  try {

    const users = await userDb.find({
      ...(!!paymentStatus && {paymentStatus})
      })
      await closeDB()
    return res.status(200).json({
      status: true,
      number:users.length,
      message: users,
      
    })
  } catch (e) {
    console.log(e)
    return res.status(500).json({
      status: false,
      error: "server error" + e,
    });
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
    res.status(404).end("Page is not found users");
  },
});
