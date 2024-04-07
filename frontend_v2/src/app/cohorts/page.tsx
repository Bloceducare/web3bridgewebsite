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
          <Button className="h-14 w-max mx-auto xl:mx-0 mt-7 xl:mt-14 px-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
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

      <MaxWrapper>
        <div></div>
      </MaxWrapper>
      <Join />
    </div>
  );
}
