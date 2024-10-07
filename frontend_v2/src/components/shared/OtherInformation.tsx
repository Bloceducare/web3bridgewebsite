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
import { Loader2, MoveRight } from "lucide-react";
import { Textarea } from "../ui/textarea";
import { useState } from "react";

export default function OtherInformation({
  step,
  setFormData,
  formData,
  isUpdatingSteps,
  submitData,
  isRegistering,
}: {
  step: number;
  setFormData: any;
  formData: any;
  isUpdatingSteps: boolean;
  isRegistering: boolean;
  submitData: () => void;
}) {
    // const router = useRouter(); 
    const [isCheckboxChecked, setIsCheckboxChecked] = useState(false);

   const form = useForm<z.infer<typeof otherSchema>>({
    resolver: zodResolver(otherSchema),
    defaultValues: {
      duration:
        formData?.course === "Web3 - Solidity" ? "4 Months" : "3 Months",
      motivation: "",
      achievement: "",
      discount: "",
      wallet_address: "",
      cta: false
    },
  });


  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof otherSchema>) {
    
    setFormData({ ...formData, ...values });

    // Check if a discount code is entered
    if (values.discount) {
      // Simulate discount code verification
      const isDiscountValid = validateDiscountCode(values.discount);
      if (!isDiscountValid) {
        alert("Invalid discount code. Please try again.");
        return;
      }
    }

    function validateDiscountCode(code: string) {
        const validCodes = ["DISCOUNT10", "WEB3BRIDGECOD3"]; 
        return validCodes.includes(code);
    }
    submitData();
    // router.push("/payment-success");
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
                    name="duration"
                    placeholder="Select training duration"
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
                  What inspired or motivated you to start writing codes?
                </FormLabel>
                <FormControl>
                  <Textarea
                    {...field}
                    cols={8}
                    rows={8}
                    name="motivation"
                    placeholder="Write here"
                    className="h-24 py-4 shadow-none px-4 text-xs md:text-sm resize-none"
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
                  MetaMask wallet address, not where you are.
                </FormDescription>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="discount"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Discount Code (Optional)
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
                    checked={isCheckboxChecked}
                    onChange={(e) => {
                      field.onChange(e);
                      setIsCheckboxChecked(e.target.checked);
                    }}
                    required
                  />
                </FormControl>
                <FormLabel className="text-xs md:text-sm font-medium">
                  (required)
                </FormLabel>

                <FormMessage />
              </FormItem>
            )}
          />

          <CustomButton
            variant="default"
            disabled={isRegistering || isUpdatingSteps || !isCheckboxChecked} // Disable if checkbox is not checked
            className="mt-10 bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:w-full md:max-w-[261px] mx-auto"
          >
            {isRegistering || isUpdatingSteps ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" /> Please wait...
              </>
            ) : (
              <>
                Proceed To Check Out <MoveRight className="w-5 h-5 ml-2" />
              </>
            )}
          </CustomButton>
        </form>
      </Form>
    </div>
  );
}
