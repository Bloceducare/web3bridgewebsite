"use client";

import { hubRegistrationSchema } from "@/lib/validators";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useState, useEffect } from "react";
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
import { Button } from "../ui/button";
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
      preferred_date: "",
      preferred_time: "",
      expected_duration_hours: 4,
    },
  });
  
  const [availableSlots, setAvailableSlots] = useState<any[]>([]);
  const [timeSlots, setTimeSlots] = useState<any[]>([]);
  const [loadingSlots, setLoadingSlots] = useState(false);
  const selectedDate = form.watch("preferred_date");
  
  // Fetch available slots when date changes
  useEffect(() => {
    if (selectedDate) {
      fetchAvailableSlots(selectedDate);
    } else {
      setAvailableSlots([]);
    }
  }, [selectedDate]);
  
  const fetchAvailableSlots = async (date: string) => {
    setLoadingSlots(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/api/v2/hub/registration/available_slots/?start_date=${date}&end_date=${date}`
      );
      const data = await response.json();
      if (data.success) {
        setAvailableSlots(data.data.available_slots || []);
        setTimeSlots(data.data.time_slots || []);
      }
    } catch (error) {
      console.error("Error fetching available slots:", error);
    } finally {
      setLoadingSlots(false);
    }
  };

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

          {/* Date and Time Selection */}
          <div className="space-y-6 pt-2 border-t">
            <h3 className="text-lg font-semibold mb-4">Select Your Preferred Visit Date & Time</h3>
            
            <FormField
              control={form.control}
              name="preferred_date"
              render={({ field }) => (
                <FormItem className="space-y-2">
                  <FormLabel className="text-sm font-medium">
                    Preferred Date <span className="text-red-500">*</span>
                  </FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="date"
                      min={new Date().toISOString().split('T')[0]}
                      className={`h-12 md:h-14 shadow-none px-4 text-sm ${
                        form.formState.errors.preferred_date ? "border-red-500" : ""
                      }`}
                      disabled={isSubmitting}
                      onChange={(e) => {
                        field.onChange(e);
                        form.setValue("preferred_time", ""); // Reset time when date changes
                      }}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {selectedDate && (
              <FormField
                control={form.control}
                name="preferred_time"
                render={({ field }) => (
                  <FormItem className="space-y-2">
                    <FormLabel className="text-sm font-medium">
                      Preferred Time <span className="text-red-500">*</span>
                    </FormLabel>
                    <FormControl>
                      {loadingSlots ? (
                        <div className="h-12 md:h-14 flex items-center justify-center border rounded-md">
                          <span className="text-sm text-muted-foreground">Loading available times...</span>
                        </div>
                      ) : availableSlots.length > 0 ? (
                        <select
                          {...field}
                          className={`h-12 md:h-14 shadow-none px-4 text-sm border rounded-md bg-background ${
                            form.formState.errors.preferred_time ? "border-red-500" : ""
                          }`}
                          disabled={isSubmitting}
                        >
                          <option value="">Select a time</option>
                          {availableSlots
                            .filter(slot => slot.date === selectedDate)
                            .map((slot) => (
                              <option key={slot.datetime} value={slot.time}>
                                {slot.time} ({slot.available_spaces} spaces available)
                              </option>
                            ))}
                        </select>
                      ) : (
                        <div className="h-12 md:h-14 flex items-center justify-center border rounded-md border-yellow-500 bg-yellow-50 dark:bg-yellow-900/10">
                          <span className="text-sm text-yellow-700 dark:text-yellow-400">
                            No available slots for this date. Please select another date.
                          </span>
                        </div>
                      )}
                    </FormControl>
                    <FormMessage />
                    {availableSlots.length > 0 && selectedDate && (
                      <p className="text-xs text-muted-foreground">
                        Available times are based on current hub capacity and existing bookings.
                      </p>
                    )}
                  </FormItem>
                )}
              />
            )}

            <FormField
              control={form.control}
              name="expected_duration_hours"
              render={({ field }) => (
                <FormItem className="space-y-2">
                  <FormLabel className="text-sm font-medium">
                    Expected Duration (hours)
                  </FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="number"
                      min={1}
                      max={12}
                      value={field.value || 4}
                      onChange={(e) => field.onChange(parseInt(e.target.value) || 4)}
                      className={`h-12 md:h-14 shadow-none px-4 text-sm ${
                        form.formState.errors.expected_duration_hours ? "border-red-500" : ""
                      }`}
                      disabled={isSubmitting}
                    />
                  </FormControl>
                  <p className="text-xs text-muted-foreground">
                    How long do you plan to stay? (Default: 4 hours)
                  </p>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <div className="pt-4">
            <Button
              type="submit"
              size="lg"
              className="w-full h-12 md:h-14 text-sm md:text-base font-semibold bg-bridgeRed hover:bg-red-600 text-white"
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
            </Button>
          </div>
        </form>
      </Form>
    </div>
  );
}

