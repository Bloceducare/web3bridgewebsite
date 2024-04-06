'use client'
import img1 from "../../../public/home/web2-arrows.png";
import img2 from "../../../public/home/web2-arrows-dark.png";
import Image from "next/image";
import { cn } from "@/lib/utils";
import { Slide } from "react-awesome-reveal";
import { Button } from "../ui/button";
import { MoveRight } from "lucide-react";

const Web2 = () => {

    const data = [
        {
            firstTitle: "Javascript",
            secondTitle: "Nodejs",
            text1: "Gain the basics and in-depth knowledge about javascript",
            text2: "Get everything you need to launch your career as a smart contract developer",
            img: img1
        },
        {
            firstTitle: "HTML & CSS",
            secondTitle: "Git & Netlify",
            text1: "Get everything you need to launch your career as a smart contract developer",
            text2: "Get everything you need to launch your career as a smart contract developer",
            img: img2
        },
        {
            firstTitle: "Typescript",
            secondTitle: "React",
            text1: "Get everything you need to launch your career as a smart contract developer",
            text2: "Get everything you need to launch your career as a smart contract developer",
            img: img1
        }
    ]
    return (
        <section className="w-full flex flex-col items-center md:gap-8 gap-8 justify-center radial-gradient lg:px-6 md:px-2">
            <div className="flex flex-col items-center gap-3 ">
                <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">The Web 2.0 Cohort</h1>
                <p className="w-full md:w-[70%] text-muted-foreground text-center">You can get all the needed trainings to make you a proficient Web Developer through our 6 months hands-on training on web 2.0 technologies.</p>
            </div>
            <main className="w-full flex flex-col items-center gap-8">
                {
                    data.map((item, index) => (
                        <Slide key={index} direction="left" className={cn("lg:w-[55%] md:w-[70%] w-full", {
                            "self-start": index === 0,
                            "self-center": index === 1,
                            "self-end": index === 2
                        })}>
                            <div key={index} className={cn("w-full flex p-6 justify-between items-center gap-4 rounded-lg bg-gradient-to-b from-red-100/80 to-transparent dark:from-red-300 ring-2 ring-red-200/90 dark:ring-bridgeRed/50")}>
                                <div className="flex flex-1 flex-col gap-2">
                                    <h3 className="font-semibold text-xl">{item.firstTitle}</h3>
                                    <p className=" text-base">{item.text1}</p>
                                </div>
                                <div className="flex w-[25%] justify-center items-center">
                                    <Image src={item.img} alt="Techs" className="w-full h-full object-contain" />
                                </div>
                                <div className="flex flex-1 flex-col gap-2">
                                    <h3 className="font-semibold text-xl">{item.secondTitle}</h3>
                                    <p className=" text-base">{item.text2}</p>
                                </div>
                            </div>
                        </Slide>
                    ))
                }
                <Button className="rounded-full mt-8 px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-bridgeRed hover:text-red-100">
                    Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
                </Button>
            </main>
        </section>
    )
}

export default Web2