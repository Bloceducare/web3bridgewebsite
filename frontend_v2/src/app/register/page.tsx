"use client";

import React, { useEffect, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import MaxWrapper from "@/components/shared/MaxWrapper";
import CustomButton from "@/components/shared/CustomButton";
import { CheckCircle, Info, Loader2, MoveRight } from "lucide-react";
import { coursesSchema, formSchema, otherSchema } from "@/lib/validators";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { Textarea } from "@/components/ui/textarea";
import SelectCourse from "@/components/shared/SelectCourse";
import PersonalInformation from "@/components/shared/PersonalInformation";
import OtherInformation from "@/components/shared/OtherInformation";
import SuccessForm from "@/components/shared/SuccessForm";
import { isValidEthereumAddress } from "@/lib/utils";
import { useFetchAllCourses, useFetchAllRegistration } from "@/hooks";

export default function RegistrationPage() {
  const { data, isLoading } = useFetchAllCourses();
  const { data: allReg, isLoading: loadReg } = useFetchAllRegistration();

  const regId = allReg?.map((item: any) => item?.id);

  const [step, setStep] = useState(1);
  const [allStatusFalse, setAllStatusFalse] = useState(1);
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

  useEffect(() => {
    if (loadReg) return;

    const allClosed = allReg.every((reg: Registration) => reg.status === false); // Adjust according to your actual data structure
    setAllStatusFalse(allClosed);
  }, [allReg, loadReg]);

  const submitData = async () => {
    if (!formData) return;
    const valid = isValidEthereumAddress(formData.wallet_address);

    const courseId = data.find((item: any) => item?.name === formData.course)?.id;

    const courseName = data.find((item: any) => item?.name === formData.course)?.name;

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

  return (
    <MaxWrapper className="flex-1 flex items-center justify-center flex-col gap-10 mt-16 md:mt-20">
      {allStatusFalse ? (
        <div className="text-center text-[2em] text-[#ff0000]">Registration Closed</div>
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
