"use client";

import { hubRegistrationSchema } from "@/lib/validators";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";
import CustomButton from "./CustomButton";
import { Loader2 } from "lucide-react";

interface HubRegistrationFormProps {
  onSubmit: (data: z.infer<typeof hubRegistrationSchema>) => void;
  isSubmitting?: boolean;
}

export default function HubRegistrationForm({
  onSubmit,
  isSubmitting = false,
}: HubRegistrationFormProps) {
  const form = useForm<z.infer<typeof hubRegistrationSchema>>({
    resolver: zodResolver(hubRegistrationSchema),
    defaultValues: {
      name: "",
      email: "",
      phone_number: "",
      location: "",
      reason: "",
      role: "",
      contribution: "",
    },
  });

  function handleSubmit(values: z.infer<typeof hubRegistrationSchema>) {
    onSubmit(values);
  }

  return (
    <div className="max-w-[680px] w-full px-4 md:px-6 py-6 md:py-8 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
      <div className="mb-6">
        <h1 className="text-xl md:text-2xl font-semibold mb-2">
          Lagos Ethereum Community Hub Registration
        </h1>
        <p className="text-sm text-muted-foreground">
          The Lagos Ethereum Community Hub is a shared space designed to support
          builders, founders, researchers, students, and community members who
          are contributing to the Ethereum ecosystem. To help us manage the
          space effectively and ensure a productive environment for everyone,
          please fill out the form below with accurate information.
        </p>
      </div>

      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(handleSubmit)}
          className="flex flex-col gap-6"
        >
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem className="space-y-2">
                <FormLabel className="text-sm font-medium">
                  Name <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    placeholder="Enter your full name"
                    className={`h-12 md:h-14 shadow-none px-4 text-sm ${
                      form.formState.errors.name ? "border-red-500" : ""
                    }`}
                    disabled={isSubmitting}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem className="space-y-2">
                <FormLabel className="text-sm font-medium">
                  Email Address <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="email"
                    placeholder="Enter your email address"
                    className={`h-12 md:h-14 shadow-none px-4 text-sm ${
                      form.formState.errors.email ? "border-red-500" : ""
                    }`}
                    disabled={isSubmitting}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="phone_number"
            render={({ field }) => (
              <FormItem className="space-y-2">
                <FormLabel className="text-sm font-medium">
                  Phone Number <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="tel"
                    placeholder="Enter your phone number"
                    className={`h-12 md:h-14 shadow-none px-4 text-sm ${
                      form.formState.errors.phone_number ? "border-red-500" : ""
                    }`}
                    disabled={isSubmitting}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="location"
            render={({ field }) => (
              <FormItem className="space-y-2">
                <FormLabel className="text-sm font-medium">
                  Location <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    placeholder="Where are you coming to the hub from?"
                    className={`h-12 md:h-14 shadow-none px-4 text-sm ${
                      form.formState.errors.location ? "border-red-500" : ""
                    }`}
                    disabled={isSubmitting}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="reason"
            render={({ field }) => (
              <FormItem className="space-y-2">
                <FormLabel className="text-sm font-medium">
                  Why do you want to come and use the hub?{" "}
                  <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Textarea
                    {...field}
                    placeholder="Please explain why you want to use the hub..."
                    className={`min-h-[100px] shadow-none px-4 py-3 text-sm resize-y ${
                      form.formState.errors.reason ? "border-red-500" : ""
                    }`}
                    disabled={isSubmitting}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="role"
            render={({ field }) => (
              <FormItem className="space-y-2">
                <FormLabel className="text-sm font-medium">
                  Describe your role in the ecosystem{" "}
                  <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    placeholder="e.g. Developer, founder, creator..."
                    className={`h-12 md:h-14 shadow-none px-4 text-sm ${
                      form.formState.errors.role ? "border-red-500" : ""
                    }`}
                    disabled={isSubmitting}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="contribution"
            render={({ field }) => (
              <FormItem className="space-y-2">
                <FormLabel className="text-sm font-medium">
                  Please share how you contribute to Ethereum{" "}
                  <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Textarea
                    {...field}
                    placeholder="Describe your contributions to the Ethereum ecosystem..."
                    className={`min-h-[120px] shadow-none px-4 py-3 text-sm resize-y ${
                      form.formState.errors.contribution
                        ? "border-red-500"
                        : ""
                    }`}
                    disabled={isSubmitting}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="pt-4">
            <CustomButton
              type="submit"
              className="w-full h-12 md:h-14 text-sm md:text-base font-medium"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Submitting...
                </>
              ) : (
                "Submit Registration"
              )}
            </CustomButton>
          </div>
        </form>
      </Form>
    </div>
  );
}

