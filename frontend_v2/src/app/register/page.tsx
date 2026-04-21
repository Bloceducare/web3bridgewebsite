"use client";
/* eslint-disable react/no-unescaped-entities */
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { MoveRight, Loader2 } from "lucide-react";
import { toast } from "sonner";
import UnifiedRegistrationForm from "@/components/shared/UnifiedRegistrationForm";
import { getCohortStatus, useFetchAllCourses } from "@/hooks";
import { buttonVariants } from "@/components/ui/button";
import dynamic from "next/dynamic";
import PaymentPendingModal from "@/components/shared/PaymentPendingModal";
import SolidityAssessmentModal from "@/components/shared/SolidityAssessmentModal";
// Types
interface FormDataType {
  email: string;
  name: string;
  github?: string;
  country: string;
  state: string;
  number: string;
  course: string;
  venue?: string;
  registration?: string;
  /** Shown on UnifiedRegistrationForm; sent to Participant create as `gender`. */
  gender: string;
}

interface UserDataType extends FormDataType {
  wallet_address: string;
  city: string;
  gender: string;
  motivation: string;
  achievement: string;
}

const CountDown = dynamic(() => import("@/components/events/CountDown"), {
  ssr: false,
});

export default function RegistrationPage() {
  const router = useRouter();
  const { data: courses, isLoading } = useFetchAllCourses();

  const [isRegistering, setIsRegistering] = useState(false);
  const [isRegistered, setIsRegistered] = useState(false);

  const [errorMessage, setErrorMessage] = useState<{
    name?: string;
    email?: string;
    github?: string;
  }>({});

  const [formData, setFormData] = useState<FormDataType | null>(null);
  const [isClose, setIsClose] = useState(false);

  // Payment pending modal state
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [paymentModalData, setPaymentModalData] = useState<{
    message: string;
    paymentLink: string;
    participantId?: string;
  } | null>(null);

  // Solidity Assessment Modal state
  const [showSolidityModal, setShowSolidityModal] = useState(false);

  // Helper function to check if a course is ZK-related (strict, excludes Rust)
  async function getUserData(userForm: UserDataType, courseName: string) {
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
      const data = await response.json();

      if (data.errors && data.errors.email && typeof data.errors.email === 'object' && data.errors.email.already_registered_unpaid) {
        if (courseName === "Solidity (Web3 Development)") {
          throw new Error("You have already registered for this course. Please check your email for assessment instructions.");
        }
        
        setPaymentModalData({
          message: data.errors.email.message,
          paymentLink: data.errors.email.payment_link,
          participantId: data.errors.email.participant_id
        });
        setShowPaymentModal(true);
        throw new Error("ALREADY_REGISTERED_UNPAID");
      }

      let errorMessages: Record<string, string[]> = {};
      if (data.errors && data.errors.email) {
        if (Array.isArray(data.errors.email)) {
          errorMessages.email = data.errors.email;
        } else if (typeof data.errors.email === 'string') {
          errorMessages.email = [data.errors.email];
        } else if (typeof data.errors.email === 'object') {
          errorMessages.email = Object.values(data.errors.email).map(String);
        }
      }

      if (data.errors && data.errors.github) {
        errorMessages.github = data.errors.github;
      }

      if (Object.keys(errorMessages).length > 0) {
        setErrorMessage({
          name: errorMessages.name?.join(", "),
          email: errorMessages.email?.join(", "),
          github: errorMessages.github?.join(", "),
        });
      }

      throw new Error(
        errorMessages.email?.join(", ") ||
          errorMessages.github?.join(", ") ||
          data.message || "Registration failed"
      );
    } else {
      setIsRegistered(false);
    }

    const savedData = await response.json();
    return savedData;
  }

  const submitData = async (values: FormDataType) => {
    try {
      setIsRegistering(true);
      const loadingToastId = toast.loading("Processing registration...");

      // Find the selected course
      const selectedCourse = courses.find(
        (item: any) => item?.name === values.course
      );

      if (!selectedCourse) {
        toast.dismiss(loadingToastId);
        throw new Error("Selected course not found");
      }

      const courseName = selectedCourse.name;

      /** Programme id from the course row (server still uses Course → registration as source of truth). */
      const registrationId = selectedCourse.registration ?? undefined;

      // Prepare user form data for API with defaults for hidden fields
      const userForm: UserDataType = {
        ...values,
        course: selectedCourse.id,
        ...(registrationId != null ? { registration: registrationId } : {}),
        // BACKEND COMPATIBILITY: Inject defaults for fields not in the simplified UI
        wallet_address: (values as any).wallet_address || "0x0000000000000000000000000000000000000000",
        city: values.state, // Default city to state name
        gender: values.gender,
        motivation: "Enrolled through simplified unified form",
        achievement: "Enrolled through simplified unified form",
        github: values.github || (courseName.toLowerCase().includes("beginner") ? "https://github.com/web3bridge" : ""),
        venue: values.venue || (selectedCourse.venue?.[0] || "online"),
      };

      localStorage.setItem("regData", JSON.stringify(userForm));

      try {
        await getUserData(userForm, courseName);
        toast.dismiss(loadingToastId);
        
        if (courseName === "Solidity (Web3 Development)") {
          toast.success("Registration successful! Preparing your assessment options...");
          setShowSolidityModal(true);
        } else {
          toast.success("Registration successful! Redirecting to payment...");
          const encodedData = btoa(JSON.stringify(userForm));
          const paymentUrl = `${
            process.env.NEXT_PUBLIC_PAYMENT_SUBDOMAIN
          }?data=${encodeURIComponent(encodedData)}`;

          setTimeout(() => {
            window.location.href = paymentUrl;
          }, 1000);
        }
      } catch (error) {
        toast.dismiss(loadingToastId);
        if (error instanceof Error) {
          if (error.message === "ALREADY_REGISTERED_UNPAID") return;
          toast.error(error.message);
        } else {
          toast.error("An unknown error occurred");
        }
      }
    } catch (error) {
      toast.error("Registration failed. Please try again");
    } finally {
      setIsRegistering(false);
    }
  };

  const openDate = new Date("2025-03-17T13:00:00");
  const currentDate = new Date();
  
  useEffect(() => {
    async function checkStatus() {
      const cohortStatus = await getCohortStatus();
      if (cohortStatus) {
        setIsClose(false);
      }

      if (currentDate > openDate) {
        setIsClose(false);
      }
      if (currentDate < openDate) {
        setIsClose(true);
      }
    }
    checkStatus();
  }, [setIsClose, currentDate, openDate]);

  if (isLoading) {
    return (
      <MaxWrapper className="flex-1 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-bridgeRed" />
          <p>Loading registration details...</p>
        </div>
      </MaxWrapper>
    );
  }

  return (
    <MaxWrapper className="flex-1 flex items-center justify-center flex-col gap-10 mt-16 md:mt-20 mb-20">
      {isClose ? (
        <div className="text-center flex flex-col items-center gap-6">
          <p className="text-center text-[2em]">Registration Opens in</p>
          <CountDown targetDate={openDate.toDateString()} />
          <a
            href="https://forms.gle/5UJ6wSx1QnkZxGPXA"
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
            Do join our Telegram group to get information on the next Cohort
          </a>
        </div>
      ) : isRegistered ? (
        <div className="text-center flex flex-col items-center gap-6 max-w-2xl px-4">
          <div className="w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-green-600 dark:text-green-400">Registration Submitted!</h2>
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6 text-left">
            <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">Next Steps</h3>
            <p className="text-blue-800 dark:text-blue-200 text-sm">
              Thank you for registering. Our team will review your application and GitHub profile. You will receive an email with further instructions.
            </p>
          </div>
          <button
            onClick={() => {
              setIsRegistered(false);
              setFormData(null);
            }}
            className="px-6 py-2 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg text-sm font-medium transition-colors"
          >
            Register for Another Course
          </button>
        </div>
      ) : (
        <UnifiedRegistrationForm
          formData={formData}
          setFormData={setFormData}
          submitData={submitData}
          isRegistering={isRegistering}
          errorMessage={errorMessage}
        />
      )}
      
      {paymentModalData && (
        <PaymentPendingModal
          isOpen={showPaymentModal}
          onClose={() => {
            setShowPaymentModal(false);
            setPaymentModalData(null);
          }}
          message={paymentModalData.message}
          paymentLink={paymentModalData.paymentLink}
          participantId={paymentModalData.participantId}
        />
      )}

      <SolidityAssessmentModal
        isOpen={showSolidityModal}
        onClose={() => setShowSolidityModal(false)}
        assessmentUrl="https://assessment-incoming.vercel.app/"
        studentName={formData?.name}
        studentEmail={formData?.email}
      />
    </MaxWrapper>


    //  <div style={{ minHeight: "100vh", background: "#fff", display: "flex", alignItems: "center", justifyContent: "center", padding: "2rem" }}>
    //   <div style={{ textAlign: "center", maxWidth: 480 }}>
    //     <div style={{ width: 64, height: 64, background: "#E24B4A", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 2rem" }}>
    //       <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    //         <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    //       </svg>
    //     </div>
    //     <h1 style={{ fontSize: 28, fontWeight: 500, color: "#E24B4A", margin: "0 0 0.75rem", letterSpacing: -0.5 }}>
    //       Registration is not open yet
    //     </h1>
    //     <p style={{ fontSize: 16, color: "#888780", margin: 0, lineHeight: 1.6 }}>
    //       Check back soon, we'll announce when spots become available.
    //     </p>
    //   </div>
    // </div>
  );
}
