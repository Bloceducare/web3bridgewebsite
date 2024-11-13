"use client";

import React, { useState } from "react";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { MoveRight } from "lucide-react";
import { toast } from "sonner";
import SelectCourse from "@/components/shared/SelectCourse";
import PersonalInformation from "@/components/shared/PersonalInformation";
import OtherInformation from "@/components/shared/OtherInformation";
import SuccessForm from "@/components/shared/SuccessForm";
import { isValidEthereumAddress } from "@/lib/utils";
import { useFetchAllCourses, useFetchAllRegistration } from "@/hooks";
import { buttonVariants } from "@/components/ui/button";
import dynamic from "next/dynamic";
const CountDown = dynamic(() => import("@/components/events/CountDown"), {
  ssr: false,
});

export default function RegistrationPage() {
  const { data, isLoading } = useFetchAllCourses();
  const { data: allReg, isLoading: loadReg } = useFetchAllRegistration();

  const regId = allReg?.map((item: any) => item?.id);

  const [step, setStep] = useState(1);
  // const [allStatusFalse, setAllStatusFalse] = useState(1);
  const [isUpdatingSteps, setIsUpdatingSteps] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [formData, setFormData] = useState<FormDataType | null>(null);

  const nextStep = () => {
    setIsUpdatingSteps(true);

    const timeout = setTimeout(() => {
      setStep((prevStep) => prevStep + 1);
      setIsUpdatingSteps(false);
    }, 2000);

    return () => clearTimeout(timeout);
  };

  interface Course {
    id: number;
    name: string;
    description: string;
    venue: string[];
    extra_info: string;
    images: {
      id: number;
      picture: string;
    }[];
    status: boolean;
  }

  interface Registration {
    id: number;
    status: boolean;
  }

  // useEffect(() => {
  //   if (loadReg) return;

  //   const allClosed = allReg.every((reg: Registration) => reg.status === false); // Adjust according to your actual data structure
  //   setAllStatusFalse(allClosed);
  // }, [allReg, loadReg]);

  const submitData = async () => {
    if (!formData) return;
    const valid = isValidEthereumAddress(formData.wallet_address);

    const courseId = data.find(
      (item: any) => item?.name === formData.course
    )?.id;

    const courseName = data.find(
      (item: any) => item?.name === formData.course
    )?.name;

    const userForm = {
      ...formData,
      course: courseId,
      registration: courseName === "Web3 - Solidity" ? regId[0] : regId[1],
    };

    if (!valid) {
      toast.error("Invalid wallet address");
      return;
    }

    try {
      setIsRegistering(true);
      toast.loading("Registering...");

      const requestOptions: any = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userForm),
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/participant/`,
        requestOptions
      );

      const result = await response.json();

      if (result.success === false) {
        console.log(result);
        return toast.error(result.message);
      }

      toast.success("Registration successful!", {
        description: `Welcome aboard, ${userForm.name.split(" ")[0]}!`,
      });
      nextStep();
      setFormData(null);
      console.log(result);
    } catch (error) {
      console.error("Error during registration:", error);
      toast.error("Oops! Something went wrong", {
        description: "Please try registering again",
      });
    } finally {
      setIsRegistering(false);
      toast.dismiss();
    }
  };

  const props = {
    step,
    nextStep,
    setFormData,
    formData,
    isUpdatingSteps,
    submitData,
    isRegistering,
  };

  const openDate = new Date("2024-10-14");
  const currentDate = new Date();
  const isClose = currentDate < openDate;

  return (
    <MaxWrapper className="flex-1 flex items-center justify-center flex-col gap-10 mt-16 md:mt-20">
      {isClose ? (
        <div className="text-center flex flex-col items-center gap-6">
          <p className="text-center text-[2em]">Registration Opens in</p>

          <CountDown targetDate={openDate.toDateString()} />

          <a
            href={"https://forms.gle/WtEw4cDfWEHQcX3h9"}
            target="_blank"
            rel="noopener noreferrer"
            className={buttonVariants({ variant: "bridgePrimary" })}
          >
            Join WaitList <MoveRight className="w-5 h-5 ml-2 " />
          </a>

          <a
            href="https://t.me/web3bridge"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm underline hover:text-bridgeRed"
          >
            Do join our telegram group to get information on next cohort
          </a>
        </div>
      ) : (
        <>
          {step === 1 ? (
            <SelectCourse {...props} />
          ) : step === 2 ? (
            <PersonalInformation {...props} />
          ) : step === 3 ? (
            <OtherInformation {...props} />
          ) : (
            <SuccessForm />
          )}
        </>
      )}
    </MaxWrapper>
  );
}
