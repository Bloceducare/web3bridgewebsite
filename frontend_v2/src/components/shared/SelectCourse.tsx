"use client";

import { useFetchAllCourses } from "@/hooks";
import { useState } from "react";
import { Label } from "../ui/label";
import { RadioGroup, RadioGroupItem } from "../ui/radio-group";
import CustomButton from "./CustomButton";
import { Loader2, MoveRight } from "lucide-react";
import { toast } from "sonner";

export default function SelectCourse({
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
  const { data, isLoading } = useFetchAllCourses();

  const [selectedOption, setSelectedOption] = useState("");

  function onSubmit(e: any) {
    e.preventDefault();
    if (!selectedOption) {
      return toast.error("You need to select a course");
    }
    nextStep();
    setFormData({ ...formData, course: selectedOption });
  }

  return (
    <div className="max-w-[529px] w-full p-5 md:p-10 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
      <div className="flex gap-4 items-center">
        <h1 className="text-lg md:text-xl font-semibold">Select Course</h1>
        {!isLoading && (
          <p className="text-[#FA0101] font-bold text-base">{step} of 3</p>
        )}
      </div>

      <form
        onSubmit={onSubmit}
        className="mt-6 flex flex-col items-center gap-4">
        <div className="flex flex-col gap-4 w-full mb-10">
          <RadioGroup
            onValueChange={(e) => setSelectedOption(e)}
            className="flex flex-col gap-3">
            {isLoading ? (
              <p>Loading...</p>
            ) : (
              data &&
              data.map((course: any) => (
                <div className="flex items-center gap-4 w-full" key={course.id}>
                  <RadioGroupItem
                    value={course.name}
                    id={course.name}
                    className="ring-1 border border-red-500 ring-red-500"
                  />
                  <Label
                    htmlFor={course.name}
                    className="font-normal capitalize">
                    {course.name}
                  </Label>
                </div>
              ))
            )}
          </RadioGroup>
        </div>

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

      {/* <Form {...form}>
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
        </form>
      </Form> */}
    </div>
  );
}
