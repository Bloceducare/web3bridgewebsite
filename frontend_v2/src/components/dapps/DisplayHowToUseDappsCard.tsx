import React from "react";
import HowToUseDappCard from "./HowToUseDappCard";
import personIcon from "../../../public/dapps/pesonIcon.png";
import stackIcon from "../../../public/dapps/stackIcon.png";
import messageIcon from "../../../public/dapps/messageIcon.png";


export const DisplayHowToUseDappCards = () => {
  return (
    <div className="flex flex-col md:grid grid-cols-2 gap-12 mt-12 justify-center lg:px-6">
    <HowToUseDappCard image={personIcon} title="Select a Compatible Wallet" description="You'll need a compatible wallet that supports the blockchain network the dApp operates on.  Download and set up your chosen wallet, ensuring you securely store your private keys."/>
    <HowToUseDappCard image={stackIcon} title="Access the dApp" description="Once your wallet is set up, visit the website or platform where the dApp is hosted. Ensure that the website is legitimate and that you're accessing the correct URL."/>
    <HowToUseDappCard image={stackIcon}  title="Connect Your Wallet" description="Connect your wallet to the platform. Follow the on-screen instructions to connect your wallet securely."/>
    <HowToUseDappCard image={messageIcon} title="Interact with the dApp" description="Depending on the dApp's purpose, you may be able to perform various actions such as trading tokens, lending or borrowing assets, playing games, or participating in decentralized finance (DeFi) protocols"/>
    </div>
  );
};
