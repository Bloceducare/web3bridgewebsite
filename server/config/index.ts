
export const webPayment = {
  naira:10000,
  USD: 20,
};

export const specialClassPayment = {
  ["Html, CSS, intro to JavaScript"]:{
    naira:50000,
    USD:70,   
  },

  ["JavaScript, react, typescript"]:{
    naira:70000,
    USD:1,
    
  },
  ["JavaScript, nodejs"]:{
    naira:70000,
    USD:100,
    
  },
  ["Go"]:{
    naira:210000,
    USD:300,
    
  },
  ["Solidity"]:{
    naira:210000,
    USD:300,
    
  },
}



  export const smsConfig = {
      email:"dev@web3bridge.com",
     password : process.env.SMS_KEY,
     "sender_name" : "Web3Bridge",
     "message" : "Welcome to Web3Bridge Special Class Training. Do check your mail for further information",
 }

 
export const mailSenderConfig = {
  from: "registration@web3bridge.com",
  emailSubject: "Acceptance Email",
  subject: "Acceptance Email",
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


 export const userEmail = {
  web2:"web2",
  web3:"web3",
  specialClass:{
    1:"webemail",
    2:"webemail",
    3:"webemail",
    4:"webemail",
    5:"webemail",
  }
 }


