import Image from "next/image";
import Header from "../../../public/dapps/Header.svg";
import { RiAppsFill } from "react-icons/ri";
import { GiGamepad } from "react-icons/gi";
import { MdPalette } from "react-icons/md";

import Pill from "../shared/pill";
import { Button } from "../ui/button";
import { MoveRight } from "lucide-react";
import { LampContainer } from "../ui/lamp";

export default function HeroSection() {
  return (
    <main className="pt-10 lg:pt-20  pb-6 ">
      <div className="w-full flex lg:flex-row flex-col gap-4 md:gap-10 justify-between items-center lg:items-start">
        <div className={`basis-1/2 light:text-[#1B1B1B] order-first`}>
          <div className="flex justify-center md:justify-start">
            {" "}
            <Pill text="Decentralized Networks" />
          </div>
          <h1 className="mb-4 mt-5 text-3xl md:text-4xl text-center md:text-left font-semibold leading-none tracking-tight">
            {/* Where We Started from */}
            Building for Your Web3 Journey!
          </h1>
          <p className="mb-2 font-light leading-12 lg:mb-8 text-center md:text-left text-md md:text-xl lg:text-2xl">
            Dapps are a growing movement of applications that use Ethereum to
            disrupt business models or invent new ones.
          </p>
          <div className="flex justify-center lg:justify-start mt-4">
            <span className="flex items-center mr-5 md:mr-10">
              <RiAppsFill className="mr-2 w-[16px] h-16px] md:w-[20px] md:h-[20px]" />
              <p className="text-[10px] sm:text-sm md:text-md">
                {" "}
                Decentralized Finance
              </p>
            </span>
            <span className="flex items-center mr-5 md:mr-10">
              <GiGamepad className="mr-2 w-[20px] h-[20px] md:w-[24px] md:h-[24px]" />
              <p className="text-[10px] sm:text-sm md:text-md">Gaming</p>
            </span>
            <span className="flex items-center">
              <MdPalette className="mr-2 w-[16px] h-16px] md:w-[20px] md:h-[20px]" />

              <p className="text-[10px] sm:text-sm md:text-md">
                {" "}
                Art and Collectibles
              </p>
            </span>
          </div>
          <div className="my-4 mt-10 hidden lg:flex lg:flex-row  items-center gap-6">
            <Button className="rounded-full px-12 py-6 md:py-8 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
              Explore dApps <MoveRight className="w-5 h-5 ml-2 " />
            </Button>

            <Button className="rounded-full px-12  py-6 md:py-8 border-2 ring-2 ring-red-300 dark:ring-red-400 border-none bg-red-500/10 text-bridgeRed hover:bg-transparent">
              Build dApps
            </Button>
          </div>
        </div>

        <div className={`relative`}>
          <LampContainer>
            <Image
              priority
              src={Header}
              alt="Story image"
              className="md:w-[580px] relative sm:top-[30px] md:top-[50px]"
            />
          </LampContainer>
          {/* <Image src={headerBg} alt="Story imag" className="absolute top-[-120px] right-20 md:w-[680px] "/> */}
        </div>
      </div>
      <div className="mb-4 mt-10 lg:mt-4 flex flex-col lg:hidden items-center gap-6">
        <Button className="rounded-full px-12 py-6 md:py-8 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
          Explore dApps <MoveRight className="w-5 h-5 ml-2 " />
        </Button>

        <Button className="rounded-full px-12  py-6 md:py-8 border-2 ring-2 ring-red-300 dark:ring-red-400 border-none bg-red-500/10 text-bridgeRed hover:bg-transparent">
          Build dApps
        </Button>
      </div>
    </main>
  );
}
