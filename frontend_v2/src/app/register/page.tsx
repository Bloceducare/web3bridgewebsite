"use client";

import React, { useEffect, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import MaxWrapper from "@/components/shared/MaxWrapper";
import CustomButton from "@/components/shared/CustomButton";
import { CheckCircle, Info, Loader2, MoveRight } from "lucide-react";
import { coursesSchema, formSchema, otherSchema } from "@/lib/validators";
import { countries } from "country-data-list";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { Textarea } from "@/components/ui/textarea";

const courses = [
  "HTML, CSS, and JavaScript",
  "Node.js and React.js with TypeScript",
  "Solidity",
  "Go-Ethereum",
];

export default function RegistrationPage() {
  const [step, setStep] = useState(1);
  const [isUpdatingSteps, setIsUpdatingSteps] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [formData, setFormData] = useState<FormDataType | null>();

  const nextStep = () => {
    setIsUpdatingSteps(true);

    const timeout = setTimeout(() => {
      setStep((prevStep) => prevStep + 1);
      setIsUpdatingSteps(false);
    }, 2000);

    return () => clearTimeout(timeout);
  };

  const submitData = async () => {
    if (!formData) return;

    try {
      setIsRegistering(true);
      toast.loading("Registering...");

      const requestOptions: any = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/registration/`,
        requestOptions
      );

      if (!response.ok) {
        console.log(response);
        throw new Error("Failed to register. Please try again.");
      }

      const result = await response.json(); // Assuming the response is JSON
      toast.success("Registration successful!", {
        description: `Welcome aboard, ${formData.name.split(" ")[0]}!`,
      });
      nextStep();
      setFormData(null);
      console.log(result);
    } catch (error) {
      console.error("Error during registration:", error);
      toast.error("Oops! Something went wrong", {
        description: "Please try registering again",
      });
    } finally {
      setIsRegistering(false);
      toast.dismiss();
    }
  };

  /**
   * Motivation: My journey into coding began with a curiosity-driven desire to enhance a game I loved playing. This initial spark evolved into a passion for problem-solving and creativity, as I discovered the power of coding to bring ideas to life. Motivated by the endless opportunities in the tech industry and the chance to contribute to innovative solutions, I continue to be inspired by the impact coding can have on shaping the future.
   * Archievement: I aim to gain a deeper understanding of decentralized technologies like blockchain and smart contracts. My goal is to develop skills that will empower me to contribute to the innovation and growth of the decentralized web, unlocking new opportunities for collaboration, transparency, and decentralization in various industries.
   * Wallet Address: 0xC0E11e7674B3267175569e1c42b85bB5554aFEB4
   */

  const props = {
    step,
    nextStep,
    setFormData,
    formData,
    isUpdatingSteps,
    submitData,
    isRegistering,
  };

  return (
    <MaxWrapper className="flex-1 flex items-center justify-center flex-col gap-10 mt-16 md:mt-20">
      {step === 1 ? (
        <SelectCourse {...props} />
      ) : step === 2 ? (
        <PersonalInformation {...props} />
      ) : (
        step === 3 && <OtherInformation {...props} />
      )}
    </MaxWrapper>
  );
}

const SelectCourse = ({
  step,
  nextStep,
  setFormData,
  formData,
  isUpdatingSteps,
}: {
  nextStep: () => void;
  step: number;
  setFormData: any;
  formData: any;
  isUpdatingSteps: boolean;
}) => {
  const form = useForm<z.infer<typeof coursesSchema>>({
    resolver: zodResolver(coursesSchema),
    defaultValues: {
      course: "HTML, CSS, and JavaScript",
    },
  });

  function onSubmit(values: z.infer<typeof coursesSchema>) {
    nextStep();
    setFormData({ ...formData, course: values.course });
  }

  return (
    <div className="max-w-[529px] w-full p-5 md:p-10 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
      <div className="flex gap-4 items-center">
        <h1 className="text-lg md:text-xl font-semibold">Select Course</h1>
        <p className="text-[#FA0101] font-bold text-base">{step} of 3</p>
      </div>

      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="mt-6 flex flex-col items-center gap-4">
          <FormField
            control={form.control}
            name="course"
            render={({ field }) => (
              <FormItem className="flex flex-col gap-4 w-full mb-10">
                <FormControl className="flex flex-col gap-4">
                  <RadioGroup
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    className="flex flex-col">
                    {courses.map((course) => (
                      <FormItem
                        className="flex items-center gap-3"
                        key={course}>
                        <FormControl>
                          <RadioGroupItem
                            value={course}
                            className="ring-1 border border-red-500 ring-red-500"
                          />
                        </FormControl>
                        <FormLabel className="font-normal">{course}</FormLabel>
                      </FormItem>
                    ))}
                  </RadioGroup>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <CustomButton
            variant="default"
            disabled={isUpdatingSteps}
            className="bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:w-full md:max-w-[261px] mx-auto">
            {isUpdatingSteps ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" /> Please wait...
              </>
            ) : (
              <>
                Continue <MoveRight className="w-5 h-5 ml-2" />
              </>
            )}
          </CustomButton>
        </form>
      </Form>
    </div>
  );
};

const PersonalInformation = ({
  step,
  nextStep,
  setFormData,
  formData,
  isUpdatingSteps,
}: {
  nextStep: () => void;
  step: number;
  setFormData: any;
  formData: any;
  isUpdatingSteps: boolean;
}) => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      number: "",
      github: "",
      country: "",
      city: "",
      gender: "male",
    },
  });

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    nextStep();
    setFormData({ ...formData, ...values });
  }

  return (
    <div className="max-w-[580px] w-full px-4 md:px-6 py-6 md:py-8 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
      <div className="flex gap-4 items-center">
        <h1 className="text-lg md:text-xl font-semibold">
          Personal Information
        </h1>
        <p className="text-[#FA0101] font-bold text-base">{step} of 3</p>
      </div>

      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="mt-6 flex flex-col items-center gap-4">
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Full Name
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    name="name"
                    placeholder="Enter your full name"
                    className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
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
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Email Address
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="email"
                    name="email"
                    placeholder="Enter your email address"
                    className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="number"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Phone Number
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="number"
                    name="number"
                    placeholder="Enter your phone number"
                    className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="github"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Github Profile Link
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    name="github"
                    placeholder="Link to your Github Profile "
                    className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="country"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Country
                </FormLabel>
                <FormControl>
                  <Select
                    name="country"
                    onValueChange={field.onChange}
                    defaultValue={field.value}>
                    <SelectTrigger className="w-full h-14">
                      <SelectValue placeholder="Enter your Country" />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.all.map((country: any, index: number) => (
                        <SelectItem
                          key={`${country.name}-${index + Math.random() * 100}`}
                          value={country.name}>
                          {country.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="city"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  City
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    name="city"
                    placeholder="Enter your city"
                    className="h-12 md:h-14 shadow-none px-4 text-xs md:text-sm"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="gender"
            render={({ field }) => (
              <FormItem className="flex items-center gap-4 w-full mb-4">
                <FormLabel className="text-[15px]">Gender:</FormLabel>
                <FormControl>
                  <RadioGroup
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    className="flex items-center">
                    <FormItem className="flex items-center space-x-2 space-y-0">
                      <FormControl>
                        <RadioGroupItem
                          value="male"
                          className="ring-1 border border-red-500 ring-red-500"
                        />
                      </FormControl>
                      <FormLabel className="font-normal">Male</FormLabel>
                    </FormItem>
                    <FormItem className="flex items-center space-x-2 space-y-0">
                      <FormControl>
                        <RadioGroupItem
                          value="female"
                          className="ring-1 border border-red-500 ring-red-500"
                        />
                      </FormControl>
                      <FormLabel className="font-normal">Female</FormLabel>
                    </FormItem>
                  </RadioGroup>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <CustomButton
            variant="default"
            disabled={isUpdatingSteps}
            className="bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:w-full md:max-w-[261px] mx-auto">
            {isUpdatingSteps ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" /> Please wait...
              </>
            ) : (
              <>
                Continue <MoveRight className="w-5 h-5 ml-2" />
              </>
            )}
          </CustomButton>
        </form>
      </Form>
    </div>
  );
};

const OtherInformation = ({
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
}) => {
  const form = useForm<z.infer<typeof otherSchema>>({
    resolver: zodResolver(otherSchema),
    defaultValues: {
      duration: "4 month",
      motivation: "",
      achievement: "",
      walletAddress: "",
    },
  });

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof otherSchema>) {
    setFormData({ ...formData, ...values });
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
          className="mt-6 flex flex-col items-center gap-4">
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
            name="walletAddress"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  Paste Wallet Address
                </FormLabel>

                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    name="walletAddress"
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

          <CustomButton
            variant="default"
            disabled={isRegistering || isUpdatingSteps}
            className="mt-10 bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:w-full md:max-w-[261px] mx-auto">
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
};
