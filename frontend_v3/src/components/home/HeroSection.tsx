"use client";
import { motion } from "framer-motion";
import { MoveRight } from "lucide-react";
import { buttonVariants } from "../ui/button";
import heroImg1 from "../../../public/home/heroimg1.png";
import heroImg2 from "../../../public/home/heroimg2.png";
import heroImg3 from "../../../public/home/heroimg3.png";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

const HeroSection = () => {
  const router = useRouter();

  return (
    <section className="flex items-center justify-center lg:h-[85vh] md:h-[50vh] h-[80vh]  w-full relative overflow-hidden">
      {/* circles */}
      <main className="w-full h-full flex justify-center items-center">
        {/* first circle  */}
        <motion.div
          className="lg:w-[900px] relative md:w-[600px] w-[350px] lg:h-[900px] md:h-[600px] h-[350px] bg-transparent md:border-4 border-2 dark:border-2 border-red-100/60 border-dashed dark:border-red-500/20 rounded-full flex justify-center items-center outline-dashed outline-2 md:outline-4 dark:outline-2 outline-red-100/50 dark:outline-red-500/15 lg:outline-offset-[120px] md:outline-offset-[80px] outline-offset-[45px]"
          animate={{ rotate: 360 }}
          transition={{
            repeat: Infinity,
            repeatType: "loop",
            ease: "linear",
            duration: 60,
          }}
        >
          <Image
            src={heroImg2}
            alt="image"
            className="w-20 h-20 rounded-full absolute top-[50%] -right-10 border-2 border-bridgeRed hidden md:block"
            priority
          />

          <Image
            src={heroImg3}
            alt="image"
            className="w-20 h-20 rounded-full absolute top-[50%] -left-10 border-2 border-bridgeRed hidden md:block"
            priority
          />

          {/* second circle  */}
          <motion.div
            className="lg:w-[650px] relative md:w-[450px] w-[270px] lg:h-[650px] md:h-[450px] h-[270px] bg-red-100/20 dark:bg-transparent md:border-4 border-2 border-dashed dark:border-2 border-red-100/80 dark:border-red-500/20 rounded-full flex justify-center items-center md:outline-none outline-dashed outline-2 outline-red-100 dark:outline-red-500/10 md:outline-offset-0  md:outline-0 outline-offset-[130px]"
            animate={{ rotate: -360 }}
            transition={{
              repeat: Infinity,
              repeatType: "reverse",
              repeatDelay: 1,
              ease: "linear",
              duration: 30,
            }}
          >
            <Image
              src={heroImg1}
              alt="image"
              className="w-16 h-16 rounded-full absolute top-[50%] -right-8 border-2 border-bridgeRed hidden md:block"
              priority
            />

            {/* third circle  */}
            <div className="lg:w-[450px] md:w-[300px] w-[190px] lg:h-[450px] md:h-[300px] h-[190px] bg-red-100/30 dark:bg-bridgeRed/10 border-4  dark:border-2 border-red-100 dark:border-red-500/20 rounded-full flex  justify-center items-center"></div>
          </motion.div>
        </motion.div>
      </main>
      {/* Overlay */}
      <main className="w-full h-full absolute top-0 left-0 flex items-center justify-center">
        <div className="lg:w-[55%] md:w-[60%] w-full flex flex-col md:gap-4 gap-6 items-center justify-center">
          <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">
            Learn, Build and Network at Web3Bridge
          </h1>
          <p className="lg:w-[85%] w-full text-muted-foreground text-center">
            Start your career in the Blockchain Development industry by
            receiving training from industry experts through our 16 weeks hands
            on bootcamp.
          </p>
          <Link
            href={"/register"}
            className={buttonVariants({
              variant: "bridgePrimary",
            })}
          >
            Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
          </Link>
          {/* <Link
            href="https://docs.google.com/forms/d/e/1FAIpQLScoch9kMWh4ZxkfJyl8IHTrXMGnJWwOjdk3HNpMApkXFEFP3g/viewform"
            target="_blank"
            rel="noreferrer"
            className="rounded-full flex items-center px-12 py-3.5 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed text-sm md:text-base capitalize hover:bg-bridgeRed dark:bg-bridgeRed dark:text-red-100 hover:text-red-100">
            Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
          </Link> */}
        </div>
      </main>
    </section>
  );
};

export default HeroSection;
