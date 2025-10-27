"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { MoveRight } from "lucide-react";
import { toast } from "sonner";
import SelectCourse from "@/components/shared/SelectCourse";
import PersonalInformation from "@/components/shared/PersonalInformation";
import OtherInformation from "@/components/shared/OtherInformation";
import { isValidEthereumAddress } from "@/lib/utils";
import {
  getCohortStatus,
  useFetchAllCourses,
  useFetchAllRegistration,
} from "@/hooks";
import { buttonVariants } from "@/components/ui/button";
import dynamic from "next/dynamic";
import PaymentPendingModal from "@/components/shared/PaymentPendingModal";

// Types
interface FormDataType {
  email: string;
  wallet_address: string;
  course: string;
  discount?: string;
  // duration?: string;
  motivation?: string;
  achievement?: string;
  cta?: boolean;
  venue?: string;
}

interface UserDataType {
  course: any;
  registration: any;
  email: string;
  wallet_address: string;
  discount?: string;
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

  console.log(courses);
  // const { data: courses, isLoading } = useFetchAllCoursesById();
  const { data: allReg, isLoading: loadReg } = useFetchAllRegistration();

  const regId = allReg?.map((item: any) => item?.id);
  const [step, setStep] = useState(1);
  const [isUpdatingSteps, setIsUpdatingSteps] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [isRegistered, setIsRegistered] = useState(false);

  const [errorMessage, setErrorMessage] = useState<{
    name?: string;
    email?: string;
    github?: string;
  }>({});

  const [formData, setFormData] = useState<FormDataType | null>(null);
  const [isClose, setIsClose] = useState(false);

  const [isDiscountChecked, setIsDiscountChecked] = useState(false);
  
  // Payment pending modal state
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [paymentModalData, setPaymentModalData] = useState<{
    message: string;
    paymentLink: string;
    participantId?: string;
  } | null>(null);

  // Helper function to check if a course is ZK-related
  const isZKCourse = (courseName: string) => {
    const zkKeywords = ['zk', 'zero knowledge', 'rust', 'blockchain protocol'];
    return zkKeywords.some(keyword => 
      courseName.toLowerCase().includes(keyword)
    );
  };

  const nextStep = () => {
    setIsUpdatingSteps(true);
    const timeout = setTimeout(() => {
      setStep((prevStep) => prevStep + 1);
      setIsUpdatingSteps(false);
    }, 2000);
    return () => clearTimeout(timeout);
  };
  const prevStep = () => {
    setIsUpdatingSteps(true);
    const timeout = setTimeout(() => {
      setStep((prevStep) => prevStep - 1);
      setIsUpdatingSteps(false);
    }, 20);
    return () => clearTimeout(timeout);
  };

  async function getUserData(userForm: UserDataType) {
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
      // console.log("Response Data:", data);

      // Check for special case: user already registered but unpaid
      if (data.errors && data.errors.email && typeof data.errors.email === 'object' && data.errors.email.already_registered_unpaid) {
        // Handle already registered but unpaid case with custom modal
        setPaymentModalData({
          message: data.errors.email.message,
          paymentLink: data.errors.email.payment_link,
          participantId: data.errors.email.participant_id
        });
        setShowPaymentModal(true);
        throw new Error("ALREADY_REGISTERED_UNPAID");
      }

      let errorMessages: Record<string, string[]> = {};
      // console.log(data.errors);
      // Check for email errors
      if (data.errors && data.errors.email) {
        // Handle both array and object formats
        if (Array.isArray(data.errors.email)) {
          errorMessages.email = data.errors.email;
        } else if (typeof data.errors.email === 'string') {
          errorMessages.email = [data.errors.email];
        } else if (typeof data.errors.email === 'object') {
          // Convert object to array of strings
          errorMessages.email = Object.values(data.errors.email).map(String);
        }
      }

      // Check for wallet_address errors
      if (data.errors && data.errors.wallet_address) {
        errorMessages.wallet_address = data.errors.wallet_address;
      }

      // Check for course errors
      if (data.errors && data.errors.course) {
        errorMessages.course = data.errors.course;
      }

      // Check for GitHub errors
      if (data.errors && data.errors.github) {
        errorMessages.github = data.errors.github;
      }

      // Check for motivation errors
      if (data.errors && data.errors.motivation) {
        errorMessages.motivation = data.errors.motivation;
      }

      // Set the error message state to display all collected error messages
      if (Object.keys(errorMessages).length > 0) {
        setErrorMessage({
          name: errorMessages.name?.join(", "),
          email: errorMessages.email?.join(", "),
          github: errorMessages.github?.join(", "),
        });
      } else {
        setErrorMessage(errorMessage);
      }

      // console.log("Collected Errors:", errorMessages);

      throw new Error(
        errorMessages.email?.join(", ") ||
          errorMessages.github?.join(", ") ||
          data.message
      );
    } else {
      setIsRegistered(false);
    }

    const savedData = await response.json();
    // console.log("Participant data saved:", savedData);
    return savedData;
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
      // console.log(courseName);

      // Prepare user form data
      const userForm = {
        ...formData,
        course: courseId,
        registration: selectedCourse.registration,
      };

      if (isDiscountChecked) {
        try {
          // Validate discount code first
          const response = await fetch(
            `${process.env.NEXT_PUBLIC_BASE_URL}/payment/discount/validate/`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ code: formData.discount }),
            }
          );

          const data = await response.json();

          if (!response.ok) {
            toast.error(data.message || "Invalid discount code");
            return;
          }

          const savedData = await getUserData(userForm);

          // If discount is not explicitly 100%, redirect to payment
          if (data.percentage !== 100) {
            localStorage.setItem("regData", JSON.stringify(userForm));
            toast.success("Registration data saved! Redirecting to payment...");

            const encodedData = btoa(JSON.stringify(userForm));
            const paymentUrl = `${
              process.env.NEXT_PUBLIC_PAYMENT_SUBDOMAIN
            }?data=${encodeURIComponent(encodedData)}`;

            setTimeout(() => {
              window.location.href = paymentUrl;
            }, 1000);
            return;
          }

          // Only for explicitly 100% discount, proceed with direct registration
          localStorage.setItem("registrationData", JSON.stringify(userForm));
          toast.success("Registration successful!");
          router.push("/success");
          return;
        } catch (error) {
          if (error instanceof Error) {
            // Handle special case for already registered but unpaid
            if (error.message === "ALREADY_REGISTERED_UNPAID") {
              // Don't show additional error, the toast was already shown
              return;
            }
            toast.error(error.message);
          }
          return;
        }
      }

      // If no discount code, proceed with registration flow
      localStorage.setItem("regData", JSON.stringify(userForm));
      try {
        const savedData = await getUserData(userForm);
        
        // Check if this is a ZK course
        if (isZKCourse(courseName)) {
          toast.success("Registration submitted successfully! Our team will review your GitHub repositories and contact you with payment details once your Rust experience is verified.");
          // For ZK courses, don't redirect to payment - just show success message
          setIsRegistered(true);
        } else {
          toast.success("Registration data saved! Redirecting to payment...");
          // For non-ZK courses, proceed with normal payment flow
          const encodedData = btoa(JSON.stringify(userForm));
          const paymentUrl = `${
            process.env.NEXT_PUBLIC_PAYMENT_SUBDOMAIN
          }?data=${encodeURIComponent(encodedData)}`;

          setTimeout(() => {
            window.location.href = paymentUrl;
          }, 1000);
        }
        // console.log("Participant data saved:", savedData);
      } catch (error) {
        if (error instanceof Error) {
          // Handle special case for already registered but unpaid
          if (error.message === "ALREADY_REGISTERED_UNPAID") {
            // Don't go back to previous step, just stop here
            return;
          }
          
          // console.log("Error saving participant data:", error);
          toast.error(
            error.message
            // errorMessage?.name ||
            //   errorMessage?.email ||
            //   errorMessage?.github ||
            //   "Error creating participant"
          );
          return prevStep();
        } else {
          toast.error("An unknown error occurred");
        }
        // console.error("Error saving participant data:", error);
      }
    } catch (error) {
      // console.error("Error during registration:", error);
      toast.error("Registration failed. Please try again");
    } finally {
      setIsRegistering(false);
      toast.dismiss();
    }
  };

  const [venue, setVenues] = useState<string[]>([]);

  useEffect(() => {
    if (!courses || courses.length === 0) {
      console.log("Courses data is not loaded yet");
      return;
    }

    if (formData?.course) {
      const selectedCourse = courses.find(
        (item: any) => item.name === formData.course
      );
      if (selectedCourse) {
        console.log("Selected Course:", selectedCourse);
        console.log("Venues:", selectedCourse.venue);
        setVenues(selectedCourse.venue || []);
      } else {
        console.log("No matching course found");
      }
    }
  }, [formData?.course, courses]);

  // console.log(venue);

  const props = {
    step,
    nextStep,
    prevStep,
    setFormData,
    venue,
    formData,
    isUpdatingSteps,
    submitData,
    isRegistering,
    isDiscountChecked,
    setIsDiscountChecked,
    setIsRegistered,
    isRegistered,
    errorMessage,
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
        <div className="text-center flex flex-col items-center gap-6 max-w-2xl">
          <div className="w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-green-600 dark:text-green-400">Registration Submitted Successfully!</h2>
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6 text-left">
            <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">What happens next?</h3>
            <ul className="space-y-2 text-blue-800 dark:text-blue-200 text-sm">
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">1.</span>
                <span>Our team will review your GitHub repositories to verify your Rust experience</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">2.</span>
                <span>Once confirmed, you'll receive a  payment link via email</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">3.</span>
                <span>Complete payment to finalize your registration</span>
              </li>
            </ul>
          </div>
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            Please ensure your GitHub profile and Rust repositories are public and accessible.
          </p>
          <button
            onClick={() => {
              setIsRegistered(false);
              setStep(1);
              setFormData(null);
            }}
            className="px-6 py-2 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg text-sm font-medium transition-colors"
          >
            Register for Another Course
          </button>
        </div>
      ) : (
        <>
          {step === 1 ? (
            <SelectCourse {...props} />
          ) : step === 2 ? (
            <PersonalInformation {...props} />
          ) : (
            <OtherInformation {...props} />
          )}
        </>
      )}
      
      {/* Payment Pending Modal */}
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
    </MaxWrapper>
  );
}
