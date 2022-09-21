
export const web2Payment = {
  naira:10000,
  USD: 20,
};


  export const smsConfig = {
      email:"dev@web3bridge.com",
     password : process.env.SMS_KEY,
     "sender_name" : "Web3Bridge",
     "message" : "Welcome to Web3Bridge Cohort VIII 2022. Do check your mail for further information",
 }

 
export const mailSenderConfig = {
  from: "registration@web3bridge.com",
  emailSubject: "Cohort VIII Registration",
  subject: "Cohort VIII Registration",
  replyTo: "registration@web3bridge.com",
};


 export const emailConfig ={
  sender:"registration@web3bridge.com",
  name:"Web3Bridge",
  replyTo:{
    email:"registration@web3bridge.com",
    name:"Support"
  }
 }

