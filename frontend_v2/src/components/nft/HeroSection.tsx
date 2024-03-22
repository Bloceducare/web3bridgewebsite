import React from 'react'
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import Image from "next/image";
import Pill from "../../../public/nfts/Pill.png";
import SemiCircle from "../../../public/nfts/Semicircle.png";
import Star from "../../../public/nfts/Star.png";
import Tube from "../../../public/nfts/Tube.png";

export default function HeroSection() {
    return (
        <section className="flex flex-col items-center justify-end lg:h-[70vh] md:h-[50vh] h-[70vh]  w-full relative radial-gradient" >
            <div className="lg:w-1/2 md:w-[70%] w-full flex flex-col items-center gap-4 justify-center">
                <h1 className="font-semibold leading-tight md:text-5xl text-3xl text-center">The <span className=" text-bridgeRed">BLOSSOMING</span> Web3bridge NFT</h1>
                <p className="text-center dark:text-muted-foreground"> The art tells the story of Web3bridge grooming developers from Africa and are all over the world literally or remotely contributing to the growth of the blockchain ecosystem.</p>
                <div className="mt-4 flex md:flex-row flex-col items-center md:gap-8 gap-4">
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
                        Mint NFT <MoveRight className="w-5 h-5 ml-2 " />
                    </Button>
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-400 border-none bg-red-500/10 text-bridgeRed hover:bg-transparent">
                        Connect Wallet
                    </Button>
                </div>
            </div>
            <Image
                priority
                src={Tube}
                alt="shape"
                className=" absolute lg:left-[17%] md:left-[10%] left-0 lg:bottom-[40%] md:bottom-[60%] bottom-[70%] md:w-[90px] w-[70px] md:h-[90px] h-[70px]"
            />
            <Image
                priority
                src={Star}
                alt="shape"
                className=" absolute lg:right-[10%] right-0 -z-10 md:z-0 opacity-30 md:opacity-100 bottom-[20%] w-[120px] h-[120px]"
            />
            <Image
                priority
                src={Pill}
                alt="shape"
                className=" absolute lg:right-[18%] right-[5%] md:bottom-[50%] bottom-[75%] scale-75"
            />
            <Image
                priority
                src={SemiCircle}
                alt="shape"
                className=" absolute md:right-[20%] right-[30%] md:bottom-[63%] bottom-[75%] scale-75"
            />
        </section>
    )
}