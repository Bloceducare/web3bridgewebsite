// import nodemailer from "nodemailer";
// import mg from "nodemailer-mailgun-transport";
import { mailSenderConfig } from "@server/config";
import emailTemplate from "@server/template";
import reportError from "@server/services/report-error"
import sendGridMail  from '@sendgrid/mail'
sendGridMail.setApiKey(process.env.SENDGRID_API_KEY as string)
import web2Db from "@server/models/web2";
import web3Db from "@server/template/web3";
import specialClassDb from "@server/models/specialClass";
import { Tracks } from "enums";



// interface ImailgunAuth {
//   auth: {
//     api_key: string | undefined;
//     domain: string | undefined;
//   };
// }
// const mailgunAuth = {
//   auth: {
//     api_key: process.env.MAILGUN_API_KEY as string,
//     domain: process.env.MAILGUN_DOMAIN as string,
//   },
// } as ImailgunAuth;

// async function wrappedSendMail(options: any) {
//   return new Promise((res, rej) => {
//     // @ts-ignore
//     let transport = nodemailer.createTransport(mg(mailgunAuth));
//     transport.sendMail(options, function (error, response) {
//       if (error) return rej(error);

//       return res(response);
//     });
//   });
// }


const template = (fileName, object)=>{

  let template =emailTemplate[fileName];
  if(!template) return;

 
  for (const key in object) {
    if (Object.prototype.hasOwnProperty.call(object, key)) {
      template =  template.replace(`{{${key}}}`, object[key])       
    }
  }
  return template;
}

 

export const sendEmail = async (data) => {
  const info = {...mailSenderConfig, ...data, };
 
 const final = {...info, to:info.email,  html:template(info.file, {name:data.name, currentTrack:data.currentTrack})}


if(!final?.file) return;

let userDb


if(final.currentTrack ==Tracks.specialClass){
  userDb = specialClassDb
  
}
if(final.currentTrack==Tracks.web2){
    userDb = web2Db
    
}

if(final.currentTrack==Tracks.web3){
    userDb = web3Db
}
 
  try {
    const response =   await sendGridMail.send(final)
    if(response?.[0]?.statusCode==202){
      await userDb.updateOne({email:data.email}, {
       $set: {acceptanceSent: true}
     })  
    }
  
    return {
      status: true,
      message: "Successfully sent email",
      data: response,
    };

  } catch (e) {
  reportError(`error sending email to ${data.email}\n environment:${process.env.NODE_ENV}\n ${e} `)
    console.log("error email", e);
    return {
      status: false,
      error: e,
    };
  }
};
