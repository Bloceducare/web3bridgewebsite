// export const isDev = false;
export const isDev = process.env.NODE_ENV === "development";

export const CURRENT_COHORT = "IX";
export const webPayment = {
  naira: isDev ? 10 : 10000,
  USD: 70,
};

export const specialClassPayment = {
  ["Html, CSS, intro to JavaScript"]: {
    naira: isDev ? 50000 : 500,
    USD: 70,
  },

  ["JavaScript, react, typescript"]: {
    naira: isDev ? 700 : 70000,
    USD: 100,
  },
  ["JavaScript, nodejs"]: {
    naira: isDev ? 700 : 70000,
    USD: 100,
  },
  ["Go"]: {
    naira: isDev ? 210 : 210000,
    USD: 300,
  },
  ["Solidity"]: {
    naira: isDev ? 210 : 210000,
    USD: 300,
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
