"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import Image from "next/image";
import Star2 from "../../../public/about/Star2.png";
import Periwinkle from "../../../public/about/Periwinkle.png";
import Star from "../../../public/about/Star.png";
import ProfileSection from "./ProfileSection";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function HeroSection() {
  const router = useRouter();

  return (
    <section className="flex flex-col items-center justify-end xl:h-[650px] lg:h-[700px] md:h-[70vh] sm:h-[60vh]  h-[550px]  w-full relative radial-gradient">
      <div className="xl:w-1/2 md:w-[80%] w-full flex flex-col items-center gap-4 justify-center mt-[30px]">
        <h1 className="font-semibold leading-tight md:text-5xl sm:text-4xl text-3xl text-center ">
          {" "}
          We Have Introduced Over 3000 Newbies To Web 3.0
        </h1>
        <p className="text-center dark:text-muted-foreground text-gray-700">
          Our alumni are doing well for themselves as blockchain developers,
          smart contract developers, blockchain auditors, backend developers and
          much more.
        </p>
        <div className="mt-4 items-center md:gap-8 gap-4">
          <Link href="/trainings">
            <Button
              onClick={() => router.push("/register")}
              className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
              Join The next Cohort <MoveRight className="w-5 h-5 ml-2 " />
            </Button>
          </Link>
        </div>
        <ProfileSection />
      </div>

      <Image
        priority
        src={Star}
        alt="shape"
        className="hidden md:block absolute lg:left-[17%] md:left-[5%] left-0 lg:bottom-[25%] md:bottom-[30%] bottom-[70%] md:w-[90px] w-[70px] md:h-[90px] h-[70px]"
      />
      <Image
        priority
        src={Star2}
        alt="shape"
        className=" absolute lg:right-[18%] right-[5%] md:bottom-[50%] top-[2%] w-[75px] md:w-fit scale-75"
      />
      <Image
        priority
        src={Periwinkle}
        alt="shape"
        className="left-[20px] sm:left-[25%] md:left-[50%] absolute top-[5%] scale-75 w-[75px] md:w-fit"
      />
    </section>
  );
}
