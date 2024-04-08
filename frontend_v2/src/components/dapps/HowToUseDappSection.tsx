import React from "react";
import DappCard from "./HowToUseDappCard";
import { DisplayHowToUseDappCards } from "./DisplayHowToUseDappsCard";

export const HowToUseDappSection = () => {
  return (
    <section className="w-full flex flex-col gap-4 justify-center md:py-20 py-3">
      <h1 className="font-semibold md:text-5xl text-2xl text-center capitalize ">
        How to Use a dApp
      </h1>
      <DisplayHowToUseDappCards />
    </section>
  );
};
