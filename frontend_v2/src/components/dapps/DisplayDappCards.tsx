import React from "react";
import DappCard from "./DappCards";
import HydroSwap from "../../../public/dapps/hydroswap.png";
import chained from "../../../public/dapps/chained.png";
import shapeDefi from "../../../public/dapps/shape-defi.png";

export const DisplayDappCards = () => {
  return (
    <section className="w-full flex items-center md:flex-row flex-col justify-center gap-8 md:py-16 py-3">
      <DappCard
        image={HydroSwap}
        description="Swap your tokens with ease. A community favorite that allows you to trade tokens with folks across the network."
        buttonText="Open Hydroswap"
        link="https://www.hydroswap.org/"
      />
        <DappCard
        image={chained}
        description="A De-Fi app built on the blockchain. Chained Thrift helps achieve financial goals through a decentralized thrift saving scheme."
        buttonText="Open Chained Thrift"
        link="/"
      />
        <DappCard
        image={shapeDefi}
        description="A De-Fi app built on the blockchain. Chained Thrift helps achieve financial goals through a decentralized thrift saving scheme."
        buttonText="Open Classmate"
        link="https://classmate-v2.web3bridge.com"
      />
    </section>
  );
};
