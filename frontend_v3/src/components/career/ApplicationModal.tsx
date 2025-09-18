"use client";

import { ApplicationForm } from "./ApplicationForm";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";

export function ApplicationModal() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant={"bridgePrimary"}>
          Apply For Job Opening
          <MoveRight className="w-5 h-5 ml-2" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[550px] bg-[#FFF3F3] dark:bg-gray-800 dark:text-white">
        <ApplicationForm />
      </DialogContent>
    </Dialog>
  );
}
