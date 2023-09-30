// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'


export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {

    let apiKey = process.env.IP_KEY;
try{
    const result = await fetch(`https://api.ipdata.co?api-key=${apiKey}`)
    .then(info=>info.json())
    .catch(e=>"Error")
    return   res.status(200).json({ data:result })
}
catch(e){
    return   res.status(500).json({ data:{} })
}

}
