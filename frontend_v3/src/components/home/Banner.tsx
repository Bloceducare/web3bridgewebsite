"use client";
import Image from "next/image";
import banner from "../../../public/home/banner.png";
import { Button, buttonVariants } from "../ui/button";
import { MoveRight } from "lucide-react";
import Link from "next/link"
import { useRouter } from "next/navigation";
import MaxWrapper from "../shared/MaxWrapper";
import { cn } from "@/lib/utils";

const Banner = () => {
  const router = useRouter();
  return (
    <section className="w-full flex flex-col py-14 justify-center items-center px-6 h-auto bg-[hsla(0,0%,6%,1)] bg-[url('/home/numbers-bg.avif')] bg-cover bg-center">
      <main className="flex w-full flex-col gap-6 items-center">
        <MaxWrapper>
          <div className="flex justify-between items-center gap-5 px-3 lg:px-0">
            <p className="font-semibold text-xl text-center bg-gradient-to-b bg-clip-text from-[hsla(40,100%,98%,1)] to-[hsla(40,100%,98%,0.67)] text-transparent">
              We’re not building talent for the future — we’re building the future with talent.
            </p>

            <Link
              href="/register"
              className={cn(buttonVariants({
                variant: "secondary"
              }),)}
              onClick={() => router.push("/register")}

            >
              Join The Next Cohort  <MoveRight className="w-5 h-5 ml-2 " />

            </Link>

            {/* <Link
            href="https://docs.google.com/forms/d/e/1FAIpQLScoch9kMWh4ZxkfJyl8IHTrXMGnJWwOjdk3HNpMApkXFEFP3g/viewform"
            target="_blank"
            rel="noreferrer"
            className="rounded-full flex items-center px-12 py-3.5 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed text-sm md:text-base capitalize hover:bg-bridgeRed dark:bg-bridgeRed dark:text-red-100 hover:text-red-100">
            Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
          </Link> */}
          </div>
        </MaxWrapper>

      </main>
    </section>
  );
};

export default Banner;
