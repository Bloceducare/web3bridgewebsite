"use client";

import React from "react";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import { useRouter } from "next/navigation";

export default function CTA() {
  const router = useRouter();
  return (
    <div className="w-full py-24 bg-[#FB8888]/10 dark:bg-[#FB8888]/5 backdrop-blur-md">
      {/* https://assets-global.website-files.com/5f6b7190899f41fb70882d08/651a02392cf2f40b253c6025_hexagon-3d.svg */}

      <MaxWrapper className="flex items-center justify-between gap-6 flex-col md:flex-row">
        <div className="flex items-center gap-4 text-center md:text-left md:w-[697px]">
          <div className="flex flex-col gap-2">
            <h1 className="text-3xl font-semibold leading-10">
              Ready to join the next cohort of learners?
            </h1>
            <p className="text-base font-normal leading-7 mt-2">
              Start your career in the Blockchain Development industry by
              receiving training from industry experts through our 16 weeks
              hands on bootcamp.
            </p>
          </div>
        </div>
        <Button
          onClick={() => router.push("/register")}
          className="h-14 px-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
          Join The next Cohort <MoveRight className="w-5 h-5 ml-2" />
        </Button>
      </MaxWrapper>
    </div>
  );
}
