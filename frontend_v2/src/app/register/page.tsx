"use client";
/* eslint-disable react/no-unescaped-entities */
import React, { useEffect, useState } from "react";
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

type RegistrationFlowMode = "new" | "existing" | null;

interface ExistingRegistrationOption {
  participant_id: number;
  name: string;
  email: string;
  payment_status: boolean;
  course: { id: number; name: string | null };
  registration: { id: number; name: string | null; cohort: string | null };
  assessment_gate?: {
    is_solidity_course: boolean;
    can_pay: boolean;
    status: "not_required" | "not_taken" | "passed" | "failed";
    message: string;
    assessment_link: string | null;
  };
  created_at: string;
}

const CountDown = dynamic(() => import("@/components/events/CountDown"), {
  ssr: false,
});

export default function RegistrationPage() {
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
  const [registrationMode, setRegistrationMode] =
    useState<RegistrationFlowMode>(null);
  const [existingEmail, setExistingEmail] = useState("");
  const [isFetchingExisting, setIsFetchingExisting] = useState(false);
  const [existingOptions, setExistingOptions] = useState<
    ExistingRegistrationOption[]
  >([]);
  const [hasSearchedExisting, setHasSearchedExisting] = useState(false);

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

  const fetchExistingRegistrations = async () => {
    const cleanEmail = existingEmail.trim().toLowerCase();
    if (!cleanEmail) {
      toast.error("Please enter your email address");
      return;
    }

    try {
      setIsFetchingExisting(true);
      setExistingOptions([]);
      setHasSearchedExisting(false);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/participant/continue-registration-options/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: cleanEmail }),
        }
      );
      const payload = await response.json();

      if (!response.ok || !payload?.success) {
        throw new Error(payload?.message || "Unable to fetch registrations");
      }

      const options = payload?.data?.options || [];
      setExistingOptions(options);
      setHasSearchedExisting(true);
      if (!options.length) {
        toast.error(
          "No active registration found for this email in the current cohort"
        );
      }
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Failed to fetch existing registrations"
      );
    } finally {
      setIsFetchingExisting(false);
    }
  };

  const continueWithExistingRegistration = (
    option: ExistingRegistrationOption
  ) => {
    if (option.payment_status) {
      toast.error("This registration is already paid");
      return;
    }
    const gate = option.assessment_gate;
    if (gate?.is_solidity_course && !gate.can_pay) {
      if (gate.status === "not_taken" && gate.assessment_link) {
        toast.error("Take and pass the assessment before payment.");
        window.location.href = gate.assessment_link;
        return;
      }
      if (gate.status === "failed") {
        toast.error("You did not pass the assessment yet.");
        return;
      }
    }
    const payload = {
      participantId: option.participant_id,
      name: option.name,
      email: option.email,
      course: option.course.id,
      registration: option.registration.id,
      source: "existing_registration",
    };
    const encodedData = btoa(JSON.stringify(payload));
    const paymentUrl = `${
      process.env.NEXT_PUBLIC_PAYMENT_SUBDOMAIN
    }?data=${encodeURIComponent(encodedData)}`;
    window.location.href = paymentUrl;
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
      ) : registrationMode === null ? (
        <div className="w-full max-w-[750px] px-4 md:px-8 py-8 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Registration
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-2 mb-8 text-sm">
            Choose whether to start a new registration or finish an existing one.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              type="button"
              onClick={() => setRegistrationMode("new")}
              className="p-5 border border-gray-200 rounded-xl text-left hover:border-bridgeRed transition-colors"
            >
              <p className="font-semibold text-base">Start New Registration</p>
              <p className="text-sm text-gray-500 mt-1">
                Go through the normal registration flow.
              </p>
            </button>
            <button
              type="button"
              onClick={() => setRegistrationMode("existing")}
              className="p-5 border border-gray-200 rounded-xl text-left hover:border-bridgeRed transition-colors"
            >
              <p className="font-semibold text-base">Finish Existing Registration</p>
              <p className="text-sm text-gray-500 mt-1">
                Find an existing registration and complete payment.
              </p>
            </button>
          </div>
        </div>
      ) : registrationMode === "new" ? (
        <div className="w-full max-w-[750px]">
          <div className="flex justify-end mb-3">
            <button
              type="button"
              onClick={() => setRegistrationMode(null)}
              className="text-sm text-gray-500 hover:text-bridgeRed"
            >
              Back to options
            </button>
          </div>
          <UnifiedRegistrationForm
            formData={formData}
            setFormData={setFormData}
            submitData={submitData}
            isRegistering={isRegistering}
            errorMessage={errorMessage}
          />
        </div>
      ) : (
        <div className="w-full max-w-[750px] px-4 md:px-8 py-8 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
          <div className="flex items-center justify-between gap-4 mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Finish Existing Registration
            </h2>
            <button
              type="button"
              onClick={() => {
                setRegistrationMode(null);
                setExistingOptions([]);
                setExistingEmail("");
                setHasSearchedExisting(false);
              }}
              className="text-sm text-gray-500 hover:text-bridgeRed"
            >
              Back
            </button>
          </div>
          <p className="text-sm text-gray-500 mb-4">
            Enter the same email you used to register and we'll find your pending registration(s) for the current cohort.
          </p>
          <div className="flex flex-col md:flex-row gap-3 mb-6">
            <input
              type="email"
              value={existingEmail}
              onChange={(e) => setExistingEmail(e.target.value)}
              placeholder="e.g. yourname@example.com"
              className="h-12 flex-1 px-4 rounded-lg border border-gray-300 bg-white"
            />
            <button
              type="button"
              onClick={fetchExistingRegistrations}
              disabled={isFetchingExisting}
              className="h-12 px-5 rounded-lg bg-bridgeRed text-white font-medium disabled:opacity-70"
            >
              {isFetchingExisting ? "Checking..." : "Fetch Registrations"}
            </button>
          </div>

          {existingOptions.length > 0 && (
            <div className="space-y-3">
              {existingOptions.map((option) => (
                <div
                  key={option.participant_id}
                  className="border border-gray-200 rounded-lg p-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3"
                >
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white">
                      {option.registration.name || "Registration"} -{" "}
                      {option.course.name || "Course"}
                    </p>
                    <p className="text-sm text-gray-500">
                      {option.email} • {option.registration.cohort || "Current Cohort"}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      Status:{" "}
                      {option.payment_status ? "Paid" : "Payment Pending"}
                    </p>
                    {option.assessment_gate?.is_solidity_course && (
                      <p className="text-xs text-gray-500 mt-1">
                        Assessment: {option.assessment_gate.message}
                      </p>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => continueWithExistingRegistration(option)}
                    disabled={
                      option.payment_status ||
                      (option.assessment_gate?.is_solidity_course === true &&
                        option.assessment_gate?.status === "failed")
                    }
                    className="h-10 px-4 rounded-md bg-bridgeRed text-white text-sm font-medium disabled:bg-gray-300"
                  >
                    {option.payment_status
                      ? "Already Paid"
                      : option.assessment_gate?.is_solidity_course &&
                          option.assessment_gate?.status === "not_taken"
                        ? "Take Assessment"
                        : option.assessment_gate?.is_solidity_course &&
                            option.assessment_gate?.status === "failed"
                          ? "Assessment Not Passed"
                          : "Continue to Payment"}
                  </button>
                </div>
              ))}
            </div>
          )}
          {hasSearchedExisting && existingOptions.length === 0 && (
            <div className="rounded-lg border border-dashed border-gray-300 p-4 text-sm text-gray-500">
              No open/current-cohort registration with a course was found for this email.
            </div>
          )}
        </div>
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
