import nodemailer from "nodemailer";
import mg from "nodemailer-mailgun-transport";
import { mailSenderConfig } from "@server/config";
import fs from "fs";
import web3Email from "@server/template/web3.js";
import web2Email from "@server/template/web2.js";

const SibApiV3Sdk = require('sib-api-v3-typescript');
 
const apiInstance = new SibApiV3Sdk.TransactionalEmailsApi();

apiInstance.setApiKey(SibApiV3Sdk.AccountApiApiKeys.apiKey, process.env.SENDINBLUE_API_KEY);


interface ImailgunAuth {
  auth: {
    api_key: string | undefined;
    domain: string | undefined;
  };
}
const mailgunAuth = {
  auth: {
    api_key: process.env.MAILGUN_API_KEY as string,
    domain: process.env.MAILGUN_DOMAIN as string,
  },
} as ImailgunAuth;

async function wrappedSendMail(options: any) {
  return new Promise((res, rej) => {
    // @ts-ignore
    let transport = nodemailer.createTransport(mg(mailgunAuth));
    transport.sendMail(options, function (error, response) {
      if (error) return rej(error);

      return res(response);
    });
  });
}


// replace with emailTemplateEmailSource with your own template
const template = (fileName, object)=>{
  let template =object.currentTrack === "web2" ? web2Email : web3Email;

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
 
  try {
    const response = await wrappedSendMail(final);
    return {
      status: true,
      message: "Successfully sent email",
      data: response,
    };
  } catch (e) {
    console.log("error email", e);
    return {
      status: false,
      error: e,
    };
  }
};
