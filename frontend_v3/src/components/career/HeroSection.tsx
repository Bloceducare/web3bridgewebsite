"use client";

import React, { useRef } from "react";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
// import Openings from "./Openings";
/* eslint-disable react/no-unescaped-entities */

export default function HeroSection() {
  // const OpeningSectionRef = useRef<HTMLElement | null>(null);
  // const handleScroll = () => {
  //   OpeningSectionRef.current?.scrollIntoView({ behavior: "smooth" });
  // };

  return (
    <>
      <section className="flex flex-col items-center justify-center xl:h-[650px] lg:h-[700px] md:h-[70vh] sm:h-[60vh]  h-[550px]  w-full relative radial-gradient">
        <div className="xl:w-1/2 md:w-[80%] w-full flex flex-col items-center gap-4 justify-center mt-[10px]">
          <h1 className="font-semibold leading-tight md:text-5xl sm:text-4xl text-3xl text-center">
            {" "}
            Join the Journey to Shape the Future with us
          </h1>
          <p className="text-center dark:text-muted-foreground">
            we believe in creating a workplace where creativity, innovation, and
            passion come together to build something extraordinary. Discover
            opportunities to grow your career and make an impact.
          </p>
          <div className="mt-4 items-center md:gap-8 gap-4">
            <Button
              // onClick={handleScroll}
              className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
              Explore Open Positions
              <MoveRight className="w-5 h-5 ml-2 " />
            </Button>
          </div>
        </div>
      </section>
      {/* <section className="hidden sm:block" ref={OpeningSectionRef}>
        <Openings />
      </section> */}
    </>
  );
}
