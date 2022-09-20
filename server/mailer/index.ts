import { emailConfig } from "@server/config";
import fs from "fs";
const SibApiV3Sdk = require('sib-api-v3-typescript');
 
const apiInstance = new SibApiV3Sdk.TransactionalEmailsApi();

apiInstance.setApiKey(SibApiV3Sdk.AccountApiApiKeys.apiKey, process.env.SENDINBLUE_API_KEY);


const emailTemplateSource =(fileName)=> fs.readFileSync(
  `${process.cwd()}/server/template/${fileName}.html`,
  "utf8"
);

// replace with emailTemplateEmailSource with your own template
const template = (fileName, object)=>{
  let template = emailTemplateSource(fileName);
  for (const key in object) {
    if (Object.prototype.hasOwnProperty.call(object, key)) {
      template =  template.replace(`{{${key}}}`, object[key])       
    }
  }
  return template;
}

 
const sendSmtpEmail = new SibApiV3Sdk.SendSmtpEmail(); 

export const sendEmail= async(data) => {
  const {name:AppName, sender, replyTo} = emailConfig
  const info = { ...data,}
  const {
    email,
    name,
    currentTrack,
    file="",
    subject="Cohort VIII Registration",
    type
  } = info

if(!file) return;

sendSmtpEmail.subject = subject;
sendSmtpEmail.htmlContent = template(file, {name, currentTrack});
sendSmtpEmail.sender = {name:AppName,email:sender};
sendSmtpEmail.to = [{email,name, type}];
sendSmtpEmail.replyTo = {email:replyTo.email,name:replyTo.name};
sendSmtpEmail.headers = {"Content-Type":"text/html; charset=iso-8859-1"};
  try{
    
const data = await apiInstance.sendTransacEmail(sendSmtpEmail)
// console.log('API called successfully. Returned data: ' + JSON.stringify(data));
return data
  }
  catch(e){
    console.log(e,'error sendin email')
    return e
  }

}