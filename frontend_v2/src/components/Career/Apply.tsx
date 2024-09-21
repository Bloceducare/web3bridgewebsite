"use client";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import { useState } from "react";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import ApplicationPortal from "./ApplicationModal";
/* eslint-disable react/no-unescaped-entities */

export default function ApplicationCTA() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <section className="bg-[#FB88880F] dark:bg-gray-900 text-black dark:text-white py-16 px-4 sm:px-6 lg:px-8">
      <div className="sm:max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between">
        <div className="mb-8 md:mb-0 md:mr-8">
          <h2 className="text-3xl font-[600] max-w-[24rem] mb-4 text-black dark:text-white">
            Ready to apply for an open position?
          </h2>
          <p className="text-base max-w-2xl text-gray-700 dark:text-gray-300">
            There must be a reason you are here. Find a role that matches your
            skills and passion, and apply today. We&apos;re excited to see what
            you&apos;ll bring to the table.
          </p>
        </div>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 dark:bg-red-500/20 text-bridgeRed dark:text-white hover:bg-transparent dark:hover:bg-transparent">
              Apply For Job Opening
              <MoveRight className="w-5 h-5 ml-2" />
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[550px] bg-[#FFF3F3] dark:bg-gray-800 dark:text-white">
            <ApplicationPortal />
          </DialogContent>
        </Dialog>
      </div>
    </section>
  );
}
