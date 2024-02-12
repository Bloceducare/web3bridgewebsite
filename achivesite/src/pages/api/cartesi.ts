import type { NextApiRequest, NextApiResponse } from "next";
import  { createRouter }  from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import web3userDb from "@server/models/cohortUsers";
import web2UserDb from "@server/models/web2";
import cartesiUserDb from "@server/models/cartesi";
import reportError from "@server/services/report-error";


const router = createRouter<NextApiRequest, NextApiResponse>();

interface IQuery {
  currentTrack?: string | string[] | undefined;
  page?: number | string;
}
router.get(async (req, res) => {
  let userDb;

    if(req.query.currentTrack === "web2"){
    userDb = web2UserDb
  }

  if(req.query.currentTrack === "web3"){
    userDb = web3userDb
  }
  if(req.query.currentTrack === "cartesi"){
    userDb =cartesiUserDb
  }
  

  const { currentTrack, page }: IQuery = req.query;

  try {
    await connectDB()
    // const users = await web3userDb.find({
    //   email:'okel@'
    //   // ...(!!currentTrack && { currentTrack }),
    // });

  const re =  await  cartesiUserDb.find({})
  
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  const template = (array)=>{
    const items = array.map(i=>`
    `)
  }


    return res.status(200).json({
      status: true,
      data:re,
    });
  } catch (e) {
    reportError
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
    res.status(404).end("Page is not found");
  },
});