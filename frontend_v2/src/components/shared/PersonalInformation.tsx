"use client";

import { formSchema } from "@/lib/validators";
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { RadioGroup, RadioGroupItem } from "../ui/radio-group";
import CustomButton from "./CustomButton";
import { Loader2, MoveRight } from "lucide-react";
import { Country, State } from "country-state-city";
import { useState } from "react";

export default function PersonalInformation({
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
}) {
  const [countryCode, setCountryCode] = useState<string>("");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      number: "",
      github:
        formData.course === "Web3 - Solidity"
          ? ""
          : "https://github.com/web3bridge",
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

  const countries = Country.getAllCountries();
  const states = State.getStatesOfCountry(countryCode);

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
          className="mt-6 flex flex-col items-center gap-4"
        >
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

          {formData.course === "Web3 - Solidity" && (
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
          )}
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
                    onValueChange={(value: string) => {
                      field.onChange(value);
                      const selectedCountry = countries.find(
                        (country) => country.name === value
                      );
                      setCountryCode(selectedCountry?.isoCode!);
                    }}
                    defaultValue={field.value}
                  >
                    <SelectTrigger className="w-full h-14">
                      <SelectValue placeholder="Choose your Country" />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.map((country: any, index: number) => (
                        <SelectItem
                          key={`${country.name}-${index + Math.random() * 100}`}
                          value={country.name}
                        >
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
            name="state"
            render={({ field }) => (
              <FormItem className="space-y-1 w-full">
                <FormLabel className="text-xs md:text-sm font-medium">
                  State
                </FormLabel>
                <FormControl>
                  <Select
                    name="state"
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <SelectTrigger className="w-full h-14">
                      <SelectValue placeholder="Choose your State" />
                    </SelectTrigger>
                    <SelectContent>
                      {states.map((state: any, index: number) => (
                        <SelectItem
                          key={`${state.name}-${index + Math.random() * 100}`}
                          value={state.name}
                        >
                          {state.name}
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
                    className="flex items-center"
                  >
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
            className="bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:w-full md:max-w-[261px] mx-auto"
          >
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
}
