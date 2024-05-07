"use client";

import CustomButton from "@/components/shared/CustomButton";
import Join from "@/components/shared/Join";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";

import b1 from "../../../public/cohorts/b-1.jpeg";
import b2 from "../../../public/cohorts/b-2.jpeg";
import b3 from "../../../public/cohorts/b-3.jpeg";
import b4 from "../../../public/cohorts/b-4.jpeg";
import b5 from "../../../public/cohorts/b-5.jpeg";
import Image from "next/image";
import { cn } from "@/lib/utils";
import Pill from "@/components/shared/pill";

import part from "../../../public/cohorts/part.svg";
import { useRouter } from "next/navigation";

const bannerImgs = [
  {
    img: b1,
    position: "-top-3 left-20",
  },
  {
    img: b2,
    position: "top-4 right-6",
  },
  {
    img: b3,
    position: "bottom-20 -right-4",
  },
  {
    img: b4,
    position: "-bottom-10 left-32",
  },
  {
    img: b5,
    position: "bottom-40 -left-16",
  },
];

export default function CohortsPage() {
  const router = useRouter();

  return (
    <div className="flex-1">
      <MaxWrapper className="py-10 md:py-20 w-full flex flex-col items-center justify-center xl:justify-between text-center xl:text-start xl:flex-row lg:gap-4 relative">
        <div className="radial-gradient flex-1 flex flex-col sm:my-2 gap-4 max-w-[790px] lg:max-w-full">
          <h1 className="text-3xl md:text-4xl lg:text-5xl lg:leading-[1.2] font-semibold">
            In 5 Years, We have had 10 Successful Cohorts
          </h1>
          <p className="w-full xl:max-w-[581px] text-sm md:text-base font-normal">
            Within 16weeks, you are going to give you an immersive learning
            experience on what it takes to be a Blockchain Developer and we are
            not just going to develop your technical skills but also help build
            your soft skills to be able to compete in the global market.
          </p>
          <Button
            onClick={() => router.push("/register")}
            className="h-14 w-max mx-auto xl:mx-0 mt-7 xl:mt-14 px-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
            Join The next Cohort <MoveRight className="w-5 h-5 ml-2" />
          </Button>
        </div>

        <div className="w-[534px] h-[534px] scale-[0.6] sm:scale-75 md:scale-100 relative rounded-full sm:mt-7 md:mt-14 xl:mt-0">
          {bannerImgs.map((img) => (
            <div
              className={cn(
                "w-[112px] h-[112px] rounded-full border-2 border-dashed border-red-500 radial-gradient absolute",
                img.position
              )}
              key={img.position}>
              <Image
                src={img.img}
                alt="banner-img"
                priority
                className="w-full h-full object-cover rounded-full"
              />
            </div>
          ))}

          <div className="w-[534px] h-[534px] linear-gradient rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
          <div className="w-[422px] h-[422px] linear-gradient rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
          <div className="w-[358px] h-[358px] linear-gradient rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>

          <div className="w-[534px] h-[534px] rotate-180 linear-gradient rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
          <div className="w-[422px] h-[422px] rotate-180 linear-gradient rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
          <div className="w-[358px] h-[358px] rotate-180 linear-gradient rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
        </div>
      </MaxWrapper>

      <MaxWrapper className="flex flex-col-reverse xl:flex-row items-center my-20 gap-6 justify-between">
        <div className="flex-1 flex flex-col gap-6 max-w-[582px] w-full">
          <h2 className="text-2xl md:text-[32px] font-semibold">
            The Latest Cohort: Cohort X!
          </h2>
          <p className="text-base md:text-xl md:leading-8 max-w-[416px]">
            We are working on building sustainable Web3 economy in Africa
            through remote and onsite Web3 development training, supporting web3
            developers and startups, and lowering barriers of entry into the
            Web3 ecosystem.
          </p>

          <div className="flex items-center mt-5">
            <Pill text="Online" />
            <Pill text="Onsite" />
          </div>
        </div>
        <div className="aspect-[1.2] w-full xl:max-w-[626px] xl:h-[383px] rounded-2xl linear-gradient">
          <Image
            src="/cohorts/img1.png"
            alt=""
            width={626}
            height={383}
            priority
            className="w-full h-full object-cover rounded-2xl"
          />
        </div>
      </MaxWrapper>

      <MaxWrapper className="flex items-center justify-center my-20">
        <div className="mx-auto max-w-[962px] flex items-center justify-center flex-col">
          <div className="w-full lg:w-[824px] linear-gradient aspect-[1.3] rounded-2xl">
            <Image
              src="/cohorts/img2.png"
              alt=""
              width={824}
              height={824}
              priority
              className="w-full h-full object-cover rounded-2xl"
            />
          </div>

          <p className="text-center text-xl font-semibold mb-7 mt-2">
            The intensive onsite web3 training going on at the facility for the
            9th cohort
          </p>

          <Button
            onClick={() => router.push("/register")}
            className="h-14 w-max mx-auto px-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
            Join The next Cohort <MoveRight className="w-5 h-5 ml-2" />
          </Button>
        </div>
      </MaxWrapper>

      <MaxWrapper className="flex flex-col my-20 md:my-44 gap-6">
        <div className="flex items-center justify-center flex-col w-full">
          <h1 className="text-3xl md:text-4xl lg:text-5xl lg:leading-[1.2] text-center font-semibold">
            How Can I Become Part of a Cohort?
          </h1>
          <p className="text-center text-base md:text-xl max-w-[470px] mt-2">
            All you need to do is APPLY. We give every application the same time
            and consideration.
          </p>
        </div>

        <div className="flex flex-col-reverse xl:flex-row items-center gap-20 justify-between mt-4 radial-gradient">
          <div className="flex flex-col pl-6 pr-2">
            <div className="flex flex-col w-full md:w-[576px] relative">
              <div className="w-[51.6px] h-[51.6px] rounded-full border-x-2 ring-2 ring-red-500 border-red-300 absolute -top-5 -left-5 bg-red-200/50 dark:bg-transparent backdrop-blur-sm flex items-center justify-center text-[28px] text-red-500 dark:text-red-100 font-semibold">
                1
              </div>
              <div className="w-full h-max p-6 bg-gradient-to-b from-red-100 to-red-50 dark:from-red-100/5 dark:to-red-50/5 rounded-xl border-2 ring-2 ring-red-200 border-red-100 dark:border-red-100/30">
                <h3 className="text-lg md:text-2xl mb-2 font-semibold">
                  Our Telegram Community
                </h3>
                <p className="text-sm md:text-base font-normal">
                  Our telegram community is open to all. You will get updates
                  and news as regarding the next cohort, as well as connecting
                  with past alumni.
                </p>
                <Button
                  onClick={() => router.push("/register")}
                  className="h-12 w-max mx-auto px-6 mt-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
                  Join Telegram <MoveRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            </div>
            {/* path */}
            <Image
              src={part}
              alt=""
              className="w-[451px] h-max object-contain ml-auto select-none -mr-2"
            />
            {/* path */}
            <div className="flex flex-col w-full md:w-[576px] relative">
              <div className="w-[51.6px] h-[51.6px] rounded-full border-x-2 ring-2 ring-red-500 border-red-300 absolute -top-5 -left-5 bg-red-200/50 dark:bg-transparent backdrop-blur-sm flex items-center justify-center text-[28px] text-red-500 dark:text-red-100 font-semibold">
                2
              </div>
              <div className="w-full h-max p-6 bg-gradient-to-b from-red-100 to-red-50 dark:from-red-100/5 dark:to-red-50/5 rounded-xl border-2 ring-2 ring-red-200 border-red-100 dark:border-red-100/30">
                <h3 className="text-lg md:text-2xl mb-2 font-semibold">
                  Application Phase
                </h3>
                <p className="text-sm md:text-base font-normal">
                  Our telegram community is open to all. You will get updates
                  and news as regarding the next cohort, as well as connecting
                  with past alumni.
                </p>
                <Button
                  onClick={() => router.push("/register")}
                  className="h-12 w-max mx-auto px-6 mt-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
                  Join Waitlist <MoveRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            </div>
            {/* path */}
            <Image
              src={part}
              alt=""
              className="w-[451px] h-max object-contain ml-auto select-none -mr-2"
            />
            {/* path */}
            <div className="flex flex-col w-full md:w-[576px] relative">
              <div className="w-[51.6px] h-[51.6px] rounded-full border-x-2 ring-2 ring-red-500 border-red-300 absolute -top-5 -left-5 bg-red-200/50 dark:bg-transparent backdrop-blur-sm flex items-center justify-center text-[28px] text-red-500 dark:text-red-100 font-semibold">
                3
              </div>
              <div className="w-full h-max p-6 bg-gradient-to-b from-red-100 to-red-50 dark:from-red-100/5 dark:to-red-50/5 rounded-xl border-2 ring-2 ring-red-200 border-red-100 dark:border-red-100/30">
                <h3 className="text-lg md:text-2xl mb-2 font-semibold">
                  Interview Phase
                </h3>
                <p className="text-sm md:text-base font-normal">
                  Our telegram community is open to all. You will get updates
                  and news as regarding the next cohort, as well as connecting
                  with past alumni.
                </p>
                <Button
                  onClick={() => router.push("/register")}
                  className="h-12 w-max mx-auto px-6 mt-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
                  Join Waitlist <MoveRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            </div>
          </div>

          <div className="w-full h-auto md:w-[548px] md:h-[731px] linear-gradient rounded-2xl">
            <Image
              src="/cohorts/img3.png"
              alt=""
              width={548}
              height={731}
              priority
              className="w-full h-full object-cover rounded-2xl"
            />
          </div>
        </div>
      </MaxWrapper>
      <Join />
    </div>
  );
}
