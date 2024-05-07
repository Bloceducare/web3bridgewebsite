"use client";

import { MoveRight } from "lucide-react";
import MaxWrapper from "../shared/MaxWrapper";
import { Button } from "../ui/button";
import { useRouter } from "next/navigation";

const Join = () => {
  const router = useRouter();

  return (
    <section className="w-full lg:py-24 py-20 bg-gradient-to-r mb-28 from-transparent to-bridgeRed/10">
      <MaxWrapper className="w-full lg:px-16 md:px-8 px-4">
        <div className="w-full flex md:flex-row flex-col gap-10 lg:gap-0 justify-between items-center">
          <div className="flex flex-col lg:w-[50%] gap-2">
            <h1 className="lg:text-4xl text-3xl font-semibold lg:w-[70%]">
              Ready to join the next cohort of learners?
            </h1>
            <p>
              Graduates from our program have gone to work with global brands
              such as Aavegotchi, Consensys, Nahmii, Nethermind, Polygon and
              lots more. So be rest assured that you are going to have the best
              learning experience with our program.
            </p>
          </div>
          <Button
            onClick={() => router.push("/register")}
            className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-transparent">
            Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
          </Button>
        </div>
      </MaxWrapper>
    </section>
  );
};

export default Join;
