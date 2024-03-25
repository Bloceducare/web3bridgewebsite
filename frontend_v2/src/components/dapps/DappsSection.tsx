import React from "react";
import { DisplayDappCards } from "./DisplayDappCards";

export const DappsSection = () => {
  return (
    <section className="w-full flex flex-col gap-4 justify-center md:py-20 py-10">
      <h1 className="font-semibold md:text-5xl text-2xl text-center capitalize ">
        Dapps We’ve Built
      </h1>
      <p className="text-md lg:text-xl font-light text-center">
        Here are some of our decentralized applications
      </p>

      <DisplayDappCards/>
    </section>
  );
};
