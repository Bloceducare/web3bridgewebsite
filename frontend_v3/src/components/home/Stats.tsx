"use client";
import { useScrollTrigger } from "@/lib/useScrollTrigger";
import { useState } from "react";
import CountUp from "react-countup";

const Stats = () => {
  const [count, setCount] = useState(0);
  const [counterOn, setCounterOn] = useState(false);
  const isScrolled = useScrollTrigger({
    onEnter: () => setCounterOn(true),
    onExit: () => {
      setCounterOn(false);
      setCount(0);
    },
  });

  return (
    <section className="w-full flex flex-col py-8 justify-center items-center px-6 h-[285px] bg-[hsla(0,0%,6%,1)] bg-[url('/home/numbers-bg.avif')] bg-cover bg-center">
      <p className="font-bold text-2xl bg-gradient-to-b text-transparent from-[hsla(40,100%,98%,1)] to-[hsla(40,100%,98%,0.67)] bg-clip-text">
        Over the years...
      </p>
      <div className="flex md:flex-row flex-col justify-center lg:gap-20 md:gap-12 gap-6 items-center lg:px-12 h-full">
        <div className="flex flex-col items-center gap-2">
          <h1 className="text-center lg:text-5xl text-4xl font-semibold bg-gradient-to-r from-[hsla(0,0%,100%,0.04)] to-[hsla(0,0%,60%,0.46)] bg-clip-text text-transparent">
            {isScrolled && (
              <CountUp
                start={0}
                end={880}
                duration={4}
                delay={0}
                useEasing={true}
              />
            )}
            +
          </h1>
          <p className="text-center  bg-gradient-to-b from-[hsla(0,0%,100%,0.1)] to-[hsla(0,0%,60%,1)] bg-clip-text text-transparent">
            Introduced into blockchain technology
          </p>
        </div>
        <div className="flex flex-col items-center gap-2">
          <h1 className="text-center lg:text-5xl text-4xl font-semibold bg-gradient-to-r from-[hsla(0,0%,100%,0.04)] to-[hsla(0,0%,60%,0.46)] bg-clip-text text-transparent">
            {isScrolled && (
              <CountUp
                start={0}
                end={1808}
                duration={4}
                delay={0}
                useEasing={true}
              />
            )}
            +
          </h1>
          <p className="text-center  bg-gradient-to-b from-[hsla(0,0%,100%,0.1)] to-[hsla(0,0%,60%,1)] bg-clip-text text-transparent ">
            Trained in web2.0 technology
          </p>
        </div>
        <div className="flex flex-col items-center gap-2">
          <h1 className="text-center lg:text-5xl text-4xl font-semibold   bg-gradient-to-r from-[hsla(0,0%,100%,0.04)] to-[hsla(0,0%,60%,0.46)] bg-clip-text text-transparent">
            {isScrolled && (
              <CountUp
                start={0}
                end={7}
                duration={5}
                delay={0}
                useEasing={true}
              />
            )}
            +
          </h1>
          <p className="text-center  bg-gradient-to-b from-[hsla(0,0%,100%,0.1)] to-[hsla(0,0%,60%,1)] bg-clip-text text-transparent">
            Ecosystem partners
          </p>
        </div>
      </div>
      <p className="text-[20px] bg-gradient-to-b text-transparent from-[hsla(40,100%,98%,1)] to-[hsla(40,100%,98%,0.67)] bg-clip-text">
        We’re not building talent for the future — we’re building the future
        with talent.
      </p>
    </section>
  );
};

export default Stats;
