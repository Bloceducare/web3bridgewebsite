"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import MaxWrapper from "@/components/shared/MaxWrapper";
import HubRegistrationForm from "@/components/shared/HubRegistrationForm";
import { toast } from "sonner";
import { hubRegistrationSchema } from "@/lib/validators";
import { z } from "zod";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function HubRegistrationPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (data: z.infer<typeof hubRegistrationSchema>) => {
    try {
      setIsSubmitting(true);
      toast.loading("Submitting your registration...");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/api/v2/hub/registration/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );

      const result = await response.json();

      if (response.ok && result.success) {
        toast.success("Registration submitted successfully!");
        // Optionally redirect to a success page
        setTimeout(() => {
          router.push("/success?type=hub");
        }, 2000);
      } else {
        // Handle validation errors
        if (result.errors) {
          const errorMessages = Object.values(result.errors).flat();
          errorMessages.forEach((msg: any) => {
            toast.error(typeof msg === "string" ? msg : "Validation error");
          });
        } else {
          toast.error(result.message || "Failed to submit registration. Please try again.");
        }
      }
    } catch (error) {
      console.error("Error submitting registration:", error);
      toast.error("An error occurred. Please try again later.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/20 py-8 md:py-12">
      <MaxWrapper>
        <div className="mb-6">
          <Link href="/hub">
            <Button variant="ghost" className="mb-4">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Hub
            </Button>
          </Link>
        </div>
        <div className="flex flex-col items-center justify-center w-full">
          <HubRegistrationForm
            onSubmit={handleSubmit}
            isSubmitting={isSubmitting}
          />
        </div>
      </MaxWrapper>
    </div>
  );
}

