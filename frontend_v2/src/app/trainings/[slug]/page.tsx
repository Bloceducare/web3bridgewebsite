"use client";

import MaxWrapper from "@/components/shared/MaxWrapper";
import Pill from "@/components/shared/pill";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { BadgeCheck, MoveRight } from "lucide-react";
import Image from "next/image";
import { useRouter } from "next/navigation";

const details = [
  {
    title: "HTML, CSS, and JavaScript",
    desc: "You'll learn how to structure and style web pages, as well as how to add interactivity and dynamic functionality with JavaScript.",
    color: "text-[#145D55]",
    style: "from-[#05FFE11F] to-[#0038FF00]",
  },
  {
    title: "Node.js and React.js with TypeScript",
    desc: "These courses will help you build scalable, efficient, and modern web applications, using cutting-edge technologies and best practices.",
    color: "text-[#99690A]",
    style: "from-[#FFAA051F] to-[#FF002E00]",
  },
  {
    title: "Solidity",
    desc: "In addition to web development, we also offer courses in Solidity , the language of the Ethereum blockchain.",
    color: "text-[#371AA9]",
    style: "from-[#3705FF1F] to-[#EB00FF00]",
  },
  {
    title: "Go-ethereum",
    desc: "Learn the new official Golang implementation of the Ethereum protocol",
    color: "text-primary",
    style: "from-[#FF05052A] to-[#FF00D600]",
  },
];

export default function Trainings() {
  const router = useRouter();

  return (
    <div className="flex flex-col">
      <MaxWrapper className="py-10 md:py-20 lg:py-28 w-full flex flex-col xl:flex-row lg:justify-between gap-4 relative">
        <div className="w-full max-w-full xl:max-w-[754px] text-center flex flex-col items-center justify-center xl:justify-start xl:items-start xl:text-start">
          <Pill text="15% Off Actual Price" />
          <div className="flex flex-col mt-2 gap-4">
            <h1 className="text-3xl md:text-4xl lg:text-5xl lg:leading-[1.2] font-semibold">
              Beginner’s Software Development
            </h1>
            <p className="w-full max-w-full xl:max-w-[581px] text-sm md:text-base lg:text-xl lg:leading-8 font-normal">
              The Web3Bridge specialized, paid, on-demand class offers a
              flexible learning schedule, allowing you to choose between morning
              and evening classes
            </p>
          </div>

          <div className="w-full aspect-video flex xl:hidden z-10 rounded-2xl mt-4 mb-3 bg-[#FB8888]/50 p-3 relative">
            <Image
              priority
              src="/trainings/b-4.jpeg"
              alt="banner-img"
              width={536}
              height={536}
              quality={100}
              className="w-full h-full object-cover rounded-2xl"
            />

            <div className="absolute bg-red-500 top-6 left-6 p-4 rounded-2xl w-max">
              <p className="text-sm md:text-base font-semibold text-white">
                15% Off Actual Price Over 120 Reviews
              </p>
            </div>
          </div>

          <ul className="list-item space-y-2 mt-5 w-full md:w-max">
            {details.map((item) => (
              <li key={item.title} className="flex items-center">
                <BadgeCheck className="w-5 h-5 mr-2 text-red-500" />
                <p className="text-sm md:text-base font-medium">{item.title}</p>
              </li>
            ))}
          </ul>

          <div className="flex items-end gap-3 mt-5 w-full md:w-max">
            <h1 className="text-2xl md:text-3xl lg:text-4xl lg:leading-[1.2] font-medium text-muted-foreground">
              $172.5
            </h1>
            <h1 className="text-2xl md:text-3xl lg:text-4xl lg:leading-[1.2] font-semibold text-red-500">
              $150
            </h1>
            <p className="text-md font-medium">Per Course</p>
          </div>

          <Button
            onClick={() => router.push("/register")}
            className="h-14 px-6 mt-7 w-full md:w-max rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
            Register For Training <MoveRight className="w-5 h-5 ml-2" />
          </Button>
        </div>

        <div className="relative hidden xl:flex flex-col justify-center mt-20">
          <div className="h-[464px] w-[597px] pl-16 relative">
            <Image
              priority
              src="/trainings/b-4.jpeg"
              alt="banner-img"
              width={597}
              height={464}
              quality={100}
              className="w-full h-full object-cover rounded-3xl"
            />

            <div className="absolute bg-gradient-to-b from-red-500 to-red-500/80 bottom-4 left-0 p-4 rounded-2xl w-full max-w-[210px]">
              <p className="text-sm md:text-base font-semibold text-white">
                15% Off Actual Price Over 120 Reviews
              </p>
            </div>
          </div>
          <p className="mt-6 text-sm font-normal">
            Don&apos;t miss out on this exciting opportunity to gain valuable
            skills and advance your career. Sign up for our specialized, paid,
            on-demand class today!
          </p>
        </div>
      </MaxWrapper>

      <MaxWrapper className="py-10 md:py-20 lg:py-28 w-full flex flex-col gap-10 items-center">
        <h1 className="font-semibold text-2xl sm:text-3xl md:text-4xl md:leading-[45px] lg:text-5xl lg:leading-[60px] text-center max-w-[1066px] w-full mx-auto">
          Practice What You&apos;ve Learned Through Hands-on Exercises and
          Projects.
        </h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-6 w-full">
          {details.map((detail) => (
            <div
              key={detail.title}
              className={cn(
                "border-2 min-h-full md:min-h-[238px] w-full h-full rounded-2xl p-4 bg-gradient-to-b",
                detail.style
              )}>
              <div className="w-full max-w-[257px]">
                <h2
                  className={cn(
                    "text-base md:text-lg mb-3 font-semibold",
                    detail.color
                  )}>
                  {detail.title}
                </h2>
                <p className="text-sm md:text-base">{detail.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </MaxWrapper>
    </div>
  );
}
