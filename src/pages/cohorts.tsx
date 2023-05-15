import React from "react";
import Image from "next/image";
import Link from "next/link";
import CohortsImage from "../../assets/cohorts/cohorts.svg";
import ProfileImg from "../../assets/cohorts/profile.svg";
import Button from "../components/Button";
import type { NextPage } from "next";

const Cohorts: NextPage = () => {
  return (
    <section className="py-4">
      <div className="w-full flex flex-wrap justify-center items-center xl:px-[10rem]">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8 md:w-[40%] lg:w-[50%] xl:w-[40%]">
          <h1 className="mb-4 text-3xl font-bold text-base90 dark:text-white10">
            Cohort Explainer
          </h1>
          <p className="text-base dark:text-[#A1A1A1] py-3 lg:text-xl">
            Do you want to build for the the blockchain?
          </p>
          <p className="text-base dark:text-[#A1A1A1] py-3 lg:text-xl">
            Do you desire to land a good paying job?
          </p>
          <p className="text-base dark:text-[#A1A1A1] py-3 lg:text-xl">
            Do you desire to upgrade from trenches?
          </p>
          <p className="text-base dark:text-[#A1A1A1] py-3 lg:text-xl">
            and you don’t know how to go about this?
          </p>
          <p className="lg:text-xl text-base dark:text-[#A1A1A1]">
            worry no more because Web3bridge can make this desires a reality.
          </p>
        </div>
        <div className="w-[80%] md:w-[40%] md:ml-10 lg:m=l-0 ">
          <Image src={CohortsImage} />
        </div>
      </div>
      <div className="px-7 sm:px-[5rem] lg:px-[12rem]">
        <h2 className="text-base90 dark:text-white10 mt-[5rem] font-bold mb-10 text-2xl">
          How?
        </h2>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
          Web3bridge runs a 16weeks cohort based training that will hold you by
          the hand to give you the right head start to launch your Blockchain
          Development as we help navigate you from the state of the known to the
          fiery edge of the unknown.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
          Within this 16weeks you are going to give you an immersive learning
          experience on what it takes to be a Blockchain Developer and we are
          not just going to develop your technical skills but also help build
          your soft skills to be able to compete in the global market.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
          Graduates from our program have gone to work with global brands such
          as Aavegotchi, Consensys, Nahmii, Nethermind, Polygon and lots more.
          So be rest assured that you are going to have the best learning
          experience with our program.
        </p>
      </div>
      <div className="flex items-center justify-center mt-16 w-ful">
        <Image src={ProfileImg} />
        <p className="text-base dark:text-white10">230+ Students enrolled</p>
      </div>

      <Button
        href="/trainings"
        class="py-2 px-12 mx-auto block mt-4 mb-40"
        content="Enroll Now"
        type="background"
      />
    </section>
  );
};

export default Cohorts;
