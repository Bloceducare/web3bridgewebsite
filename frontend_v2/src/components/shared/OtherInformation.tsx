"use client";

import { otherSchema } from "@/lib/validators";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useRouter } from "next/navigation";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";
import { Input } from "../ui/input";

import CustomButton from "./CustomButton";
import { Loader2, MoveRight, MoveLeft } from "lucide-react";
import { Textarea } from "../ui/textarea";
import { useState } from "react";

export default function OtherInformation({
  step,
  setFormData,
  prevStep,
  formData,
  isUpdatingSteps,
  submitData,
  isRegistering,
  isDiscountChecked,
  setIsDiscountChecked,
}: {
  step: number;
  setFormData: any;
  formData: any;
  prevStep: () => void;
  isUpdatingSteps: boolean;
  isRegistering: boolean;
  isDiscountChecked: boolean;
  setIsDiscountChecked: any;
  submitData: () => void;
}) {
  // const router = useRouter();
  const [isCheckboxChecked, setIsCheckboxChecked] = useState(false);

  const form = useForm<z.infer<typeof otherSchema>>({
    resolver: zodResolver(otherSchema),
    defaultValues: {
      duration:
        formData?.course === "Web3 - Solidity" ? "4 Months" : "3 Months",
      motivation: formData?.motivation || "",
      achievement: formData?.achievement || "",
      discount: formData?.discount || "",
      wallet_address: formData?.wallet_address || "",
      cta: formData?.cta || false,
    },
  });

  async function onSubmit(values: z.infer<typeof otherSchema>) {
    // Update form data in parent component
    setFormData({ ...formData, ...values });

    // Call parent's submitData function which handles the API validation and submission
    submitData();
  }

  return (
    <div className="max-w-[580px] w-full px-4 md:px-6 py-6 md:py-8 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
      <div className="flex gap-4 items-center">
        <h1 className="text-lg md:text-xl font-semibold">Other Information</h1>
        <p className="text-[#FA0101] font-bold text-base">{step} of 3</p>
      </div>

      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="mt-6 flex flex-col items-center gap-4"
        >
          <FormField
            control={form.control}
            name="duration"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Training Time
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    disabled={true}
                    name="duration"
                    // placeholder="Select training duration"
                    className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="motivation"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  What inspired or motivated you to start writing code?
                </FormLabel>
                <FormControl>
                  <Textarea
                    {...field}
                    cols={8}
                    rows={8}
                    name="motivation"
                    placeholder="Write here"
                    className="h-24 py-4 shadow-none px-4 text-xs md:text-sm resize-none"
                    maxLength={100}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="achievement"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  What do you hope to achieve from this program?
                </FormLabel>
                <FormControl>
                  <Textarea
                    {...field}
                    name="achievement"
                    placeholder="Write here"
                    className="h-24 py-4 shadow-none px-4 text-xs md:text-sm resize-none"
                    maxLength={100}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="wallet_address"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Paste Wallet Address
                </FormLabel>

                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    name="wallet_address"
                    autoComplete="off"
                    placeholder="Paste your wallet address"
                    className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
                  />
                </FormControl>
                <FormMessage />
                <FormDescription className="text-xs md:text-sm">
                  Please be aware that the address you are to provide is your
                  MetaMask wallet address, not where you live.
                </FormDescription>
              </FormItem>
            )}
          />
          <div className="flex items-center space-y-1 w-full">
            <label>
              <input
                className="me-1"
                type="checkbox"
                checked={isDiscountChecked}
                onChange={(e) => setIsDiscountChecked(e.target.checked)}
              />
              Do you have a discount Code?
            </label>
          </div>
          {isDiscountChecked ? (
            <FormField
              control={form.control}
              name="discount"
              render={({ field }) => (
                <FormItem className="space-y-1 w-full">
                  <FormLabel className="text-xs md:text-sm font-medium">
                    {/* Discount Code */}
                  </FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      type="text"
                      name="discount"
                      placeholder="Enter discount code..."
                      className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          ) : (
            ""
          )}
          <FormField
            control={form.control}
            name="cta"
            render={({ field }) => (
              <FormItem className="flex items-center space-y-1 w-full">
                <FormControl>
                  <Input
                    {...field}
                    type="checkbox"
                    name="cta"
                    className="h-5 w-5 mr-2"
                    id="cta"
                    value="true"
                    checked={Boolean(field.value)}
                    onChange={(e) => {
                      field.onChange(e.target.checked);
                      setIsCheckboxChecked(e.target.checked);
                    }}
                    required
                  />
                </FormControl>
                <FormLabel className="text-xs md:text-sm font-medium">
                  Please confirm that you have access to the secret key
                  associated with your wallet to proceed with the transaction.
                </FormLabel>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormDescription className="text-[#FA0101] font-bold text-sm">
            Please do not close this webpage or your browser application
            during/after payment until you are redirected back to this website
            and your registration is fully confirmed.
          </FormDescription>
          {isDiscountChecked ? (
            <CustomButton
              variant="default"
              disabled={
                isRegistering ||
                isUpdatingSteps ||
                !isCheckboxChecked ||
                !isDiscountChecked
              } // Disable if checkbox is not checked
              className="mt-10 bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:w-full md:max-w-[261px] mx-auto"
            >
              Complete registration
            </CustomButton>
          ) : (
            <div className="flex flex-row gap-3 w-full">
              {step > 1 && (
                <CustomButton
                  onClick={prevStep}
                  variant="outline"
                  className="bg-[#FB8888]/10 mt-10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:max-w-[261px] mx-auto text-sm"
                >
                  <MoveLeft className="w-4 h-4 mr-2" /> Previous
                </CustomButton>
              )}
              <CustomButton
                variant="default"
                disabled={
                  isRegistering || isUpdatingSteps || !isCheckboxChecked
                }
                className="mt-10 bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:max-w-[261px] mx-auto text-sm"
              >
                {isRegistering || isUpdatingSteps ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Please
                    wait...
                  </>
                ) : (
                  <>
                    Check Out
                    <MoveRight className="w-4 h-4 ml-2" />
                  </>
                )}
              </CustomButton>
            </div>
          )}
        </form>
      </Form>
    </div>
  );
}
