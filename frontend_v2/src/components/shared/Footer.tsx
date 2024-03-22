import React from "react";
import MaxWrapper from "./MaxWrapper";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-[#6E6E6E]/70 w-full py-10 bg-gradient-to-b from-red-100 via-red-200 to-background">
      <MaxWrapper className="flex gap-10">
        <div className="w-[451px] rounded-2xl bg-[#1B1B1B] p-6 flex flex-col gap-2">
          <h1 className="font-bold text-2xl text-[#FFFBF3]">
            Subscribe To Our <br /> Newsletter
          </h1>
          <p className="text-base text-[#FFFBF3] font-normal">
            Get occasional news and update from us about the latest trends,
            technology in the web 3 world, we promise not to spam you.
          </p>

          <div className="mt-14 flex items-center gap-4">
            <Input
              placeholder="Email address"
              className="rounded-full h-12 px-4"
            />
            <Button className="h-12 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-white hover:bg-transparent">
              Subscribe <MoveRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </div>

        <div className="bg-white/90 backdrop-blur-md h-full flex-1 p-6 rounded-2xl"></div>
      </MaxWrapper>
    </footer>
  );
}
