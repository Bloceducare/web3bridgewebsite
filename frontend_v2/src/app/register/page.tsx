"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { MoveRight } from "lucide-react";
import { toast } from "sonner";
import SelectCourse from "@/components/shared/SelectCourse";
import PersonalInformation from "@/components/shared/PersonalInformation";
import OtherInformation from "@/components/shared/OtherInformation";
import { isValidEthereumAddress } from "@/lib/utils";
import { useFetchAllCourses, useFetchAllRegistration } from "@/hooks";
import { buttonVariants } from "@/components/ui/button";
import dynamic from "next/dynamic";

// Types
interface FormDataType {
  email: string;
  wallet_address: string;
  course: string;
  discount?: string;
  duration?: string;
  motivation?: string;
  achievement?: string;
  cta?: boolean;
}

const CountDown = dynamic(() => import("@/components/events/CountDown"), {
  ssr: false,
});

export default function RegistrationPage() {
  const router = useRouter();
  const { data: courses, isLoading } = useFetchAllCourses();
  const { data: allReg, isLoading: loadReg } = useFetchAllRegistration();

  const regId = allReg?.map((item: any) => item?.id);
  const [step, setStep] = useState(1);
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

  async function validateDiscountCode(code: string, email: string): Promise<boolean> {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/payment/discount/validate/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ code, email }),
        }
      );

      const data = await response.json();
      console.log("Discount validation response:", data); // For debugging

      // If the API returns success: true, consider it valid
      if (data.success === true) {
        return true;
      }

      // Show appropriate error messages
      if (data.data?.is_used) {
        toast.error("This discount code has already been used");
      } else {
        toast.error("Invalid discount code");
      }

      return false;
    } catch (error) {
      console.error("Error validating discount code:", error);
      toast.error("Error validating discount code. Please try again.");
      return false;
    }
  }

  const submitData = async () => {
    if (!formData) {
      toast.error("Please fill in all required fields");
      return;
    }

    const valid = isValidEthereumAddress(formData.wallet_address);
    if (!valid) {
      toast.error("Invalid wallet address");
      return;
    }

    try {
      setIsRegistering(true);
      toast.loading("Processing registration...");

      // Find the selected course
      const selectedCourse = courses.find(
        (item: any) => item?.name === formData.course
      );

      if (!selectedCourse) {
        throw new Error("Selected course not found");
      }

      const courseId = selectedCourse.id;
      const courseName = selectedCourse.name;

      // Prepare user form data
      const userForm = {
        ...formData,
        course: courseId,
        registration: courseName === "Web3 - Solidity" ? regId[0] : regId[1],
      };

      // Validate discount code if provided
      if (formData.discount) {
        console.log("Validating discount code:", formData.discount);
        const isDiscountValid = await validateDiscountCode(formData.discount, formData.email);
        console.log("Discount validation result:", isDiscountValid);

        if (!isDiscountValid) {
          setIsRegistering(false);
          toast.dismiss();
          return;
        }

        try {
          // Save form data to the endpoint
          const response = await fetch(
            `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/participant/`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(userForm),
            }
          );

          if (!response.ok) {
            throw new Error("Failed to save participant data");
          }

          const savedData = await response.json();
          console.log("Participant data saved:", savedData);

          // Save to localStorage and show success message
          localStorage.setItem("registrationData", JSON.stringify(userForm));
          toast.success("Registration successful!");

          // Optional: Redirect to a thank you or confirmation page
          router.push("/success");
          return;
        } catch (error) {
          console.error("Error saving participant data:", error);
          toast.error("Failed to save registration data. Please try again.");
          return;
        }
      }

      // If no discount code, proceed with normal payment flow
      localStorage.setItem("registrationData", JSON.stringify(userForm));

      const encodedData = btoa(JSON.stringify(userForm));
      const paymentUrl = `${
        process.env.NEXT_PUBLIC_PAYMENT_SUBDOMAIN
      }?data=${encodeURIComponent(encodedData)}`;

      toast.success("Registration data saved! Redirecting to payment...");

      setTimeout(() => {
        window.location.href = paymentUrl;
      }, 1000);
    } catch (error) {
      console.error("Error during registration:", error);
      toast.error("Registration failed. Please try again");
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

  if (isLoading || loadReg) {
    return (
      <MaxWrapper className="flex-1 flex items-center justify-center">
        <div>Loading...</div>
      </MaxWrapper>
    );
  }

  return (
    <MaxWrapper className="flex-1 flex items-center justify-center flex-col gap-10 mt-16 md:mt-20">
      {isClose ? (
        <div className="text-center flex flex-col items-center gap-6">
          <p className="text-center text-[2em]">Registration Opens in</p>
          <CountDown targetDate={openDate.toDateString()} />
          <a
            href="https://forms.gle/WtEw4cDfWEHQcX3h9"
            target="_blank"
            rel="noopener noreferrer"
            className={buttonVariants({ variant: "bridgePrimary" })}>
            Join WaitList <MoveRight className="w-5 h-5 ml-2 " />
          </a>
          <a
            href="https://t.me/web3bridge"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm underline hover:text-bridgeRed">
            Do join our telegram group to get information on the next cohort
          </a>
        </div>
      ) : (
        <>
          {/* {step === 1 ? (
            <SelectCourse {...props} />
          ) : step === 2 ? (
            <PersonalInformation {...props} />
          ) : (
            <OtherInformation {...props} />
          )} */}
        </>
      )}
    </MaxWrapper>
  );
}
