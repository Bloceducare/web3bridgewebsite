
export const web2Payment = {
  naira:10000,
  USD: 20,
};

export const mailSenderConfig = {
    from: "info@sandbox6c3d0653cf6f40f8bd343b3dab567016.mailgun.org",
    emailSubject: "",
    replyTo: "",
  };

  export const smsConfig = {
      email:"dev@web3bridge.com",
     password : process.env.SMS_KEY,
     "sender_name" : "Web3Bridge",
     "message" : "Welcome to Web3Bridge Cohort VIII 2022. Do check your mail for further information",
 }

 export const emailConfig ={
  sender:"registration@web3bridge.com",
  name:"Web3Bridge",
  replyTo:{
    email:"registration@web3bridge.com",
    name:"Support"
  }
 }

