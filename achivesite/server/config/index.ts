// export const isDev = false;
export const isDev = process.env.NODE_ENV === "development";

export const CURRENT_COHORT = "X";
export const webPayment = {
  naira: isDev ? 10 : 10000,
  USD: 70,
};

export const specialClassPayment = {
  ["Html, CSS, intro to JavaScript"]: {
    naira: isDev ? 500 : 142500,
    USD: 150,
  },

  ["JavaScript, react, typescript"]: {
    naira: isDev ? 700 : 142500,
    USD: 150,
  },
  ["JavaScript, nodejs"]: {
    naira: isDev ? 700 : 142500,
    USD: 150,
  },
  ["GETH"]: {
    naira: isDev ? 210 : 475000,
    USD: 500,
  },
  ["Solidity"]: {
    naira: isDev ? 210 : 475000,
    USD: 500,
  },
};

export const smsConfig = {
  email: "dev@web3bridge.com",
  password: process.env.SMS_KEY,
  sender_name: "Web3Bridge",
  message:
    "Welcome to Web3Bridge Special Class Training. Do check your mail for further information",
};

export const mailSenderConfig = {
  from: { email: "registration@web3bridge.com", name: "Web3bridge" },
  emailSubject: "Acceptance Email",
  subject: "Application Received",
  replyTo: "registration@web3bridge.com",
};

export const emailConfig = {
  sender: "registration@web3bridge.com",
  name: "Web3Bridge",
  replyTo: {
    email: "registration@web3bridge.com",
    name: "Support",
  },
};

export const userEmail = {
  web2: "web2",
  web3: "web3",
  specialClass: {
    1: "webemail",
    2: "webemail",
    3: "webemail",
    4: "webemail",
    5: "webemail",
  },
};
