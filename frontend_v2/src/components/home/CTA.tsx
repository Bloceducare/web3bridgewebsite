"use client";
import { Button } from "../ui/button";
import { MoveRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { Fade } from "react-awesome-reveal";

const CTA = () => {
  const router = useRouter();

  return (
    <Fade direction="up">
      <main className="w-full flex flex-col gap-8 items-center lg:mt-56 mt-12 z-10">
        <div className="w-full lg:w-[40%] md:w-[60%] p-6 rounded-lg bg-red-50/80 ring-2 ring-red-200/80 dark:bg-transparent dark:ring-bridgeRed/40">
          <p className="text-center">
            You can chose between an onsite and an online training. Feeding,
            accommodation and internet are provided for our onsite students.
          </p>
        </div>
        <Button
          onClick={() => router.push("/register")}
          className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-bridgeRed hover:text-red-100">
          Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
        </Button>
        {/* <Link
            href="https://docs.google.com/forms/d/e/1FAIpQLScoch9kMWh4ZxkfJyl8IHTrXMGnJWwOjdk3HNpMApkXFEFP3g/viewform"
            target="_blank"
            rel="noreferrer"
            className="rounded-full flex items-center px-12 py-3.5 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed text-sm md:text-base capitalize hover:bg-bridgeRed dark:bg-bridgeRed dark:text-red-100 hover:text-red-100">
            Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
          </Link> */}
      </main>
    </Fade>
  );
};

export default CTA;
