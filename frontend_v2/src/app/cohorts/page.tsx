import CustomButton from "@/components/shared/CustomButton";
import Join from "@/components/shared/Join";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";

export default function CohortsPage() {
  return (
    <div className="flex-1">
      <MaxWrapper className="py-10 md:py-20 w-full flex items-center justify-between gap-4 relative">
        <div className="radial-gradient w-full max-w-[727px] flex flex-col my-2 gap-4">
          <h1 className="text-3xl md:text-4xl lg:text-5xl leading-10 font-semibold">
            In 5 Years, We have had 10 Successful Cohorts
          </h1>
          <p className="w-full max-w-[581px] text-sm md:text-base font-normal">
            Within 16weeks, you are going to give you an immersive learning
            experience on what it takes to be a Blockchain Developer and we are
            not just going to develop your technical skills but also help build
            your soft skills to be able to compete in the global market.
          </p>
          <Button className="h-14 w-max mt-14 px-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
            Join The next Cohort <MoveRight className="w-5 h-5 ml-2" />
          </Button>
        </div>

        <div className="w-[534px] h-[534px] bg-red-500 rounded-full"></div>
      </MaxWrapper>

      <MaxWrapper>
        <div></div>
      </MaxWrapper>
      <Join />
    </div>
  );
}
