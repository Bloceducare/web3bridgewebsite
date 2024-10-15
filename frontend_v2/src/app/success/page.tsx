"use client";

import { useEffect, useState, useRef } from "react";
import axios from "axios";
import { toast } from "sonner";
import MaxWrapper from "@/components/shared/MaxWrapper";
import SuccessForm from "@/components/shared/SuccessForm";

export default function Page() {
  const [isClient, setIsClient] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const saveInProgress = useRef(false);

  // Retrieve data from localStorage
  const retrieveDataFromLocalStorage = () => {
    const savedData = localStorage.getItem("registrationData");
    if (savedData) {
      try {
        return JSON.parse(savedData);
      } catch (error) {
        console.error("Error parsing localStorage data:", error);
        toast.error("Error retrieving registration data.");
        return null;
      }
    } else {
      toast.error("No registration data found. Please try registering again.");
      return null;
    }
  };

  // Function to check payment status
  const checkPaymentStatus = async (email: string) => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_PAYMENT_SUBDOMAIN_VERIFY}api/validate/${email}`
      );
      console.log("Payment status response:", response);

      if (response.status === 200 && response.data.status === true) {
        return true;
      } else {
        throw new Error("Payment not successful");
      }
    } catch (error) {
      console.error("Error checking payment status:", error);
      toast.error("Payment not successful. Please complete payment first.");
      return false;
    }
  };

  // Function to save data to the database
  const saveToDatabase = async (data: any) => {
    if (saveInProgress.current) return;
    setIsSaving(true);
    saveInProgress.current = true;
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/participant/`,
        data
      );

      if (response.status === 200 || response.status === 201) {
        toast.success("Registration data saved successfully!");
        localStorage.removeItem("registrationData");
      } else {
        throw new Error("Unexpected response from server.");
      }
    } catch (error) {
      const errorMessage =
        (error as any).response?.data?.message || (error as any).message;
      toast.error(`Error saving data: ${errorMessage}`);
    } finally {
      setIsSaving(false);
      saveInProgress.current = false;
    }
  };

  // Ensure client-side rendering
  useEffect(() => {
    setIsClient(true);

    const data = retrieveDataFromLocalStorage();
    if (data) {
      const { email } = data;
      checkPaymentStatus(email).then((isPaymentSuccessful) => {
        if (isPaymentSuccessful && !saveInProgress.current) {
          saveToDatabase(data);
        }
      });
    }
  }, []);

  if (!isClient) {
    return null;
  }

  return (
    <MaxWrapper className="flex-1 flex items-center justify-center flex-col gap-10 mt-16 md:mt-20">
      {isSaving ? <p>Saving your registration data...</p> : <SuccessForm />}
    </MaxWrapper>
  );
}
