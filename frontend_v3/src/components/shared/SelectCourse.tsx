"use client";

import { useFetchAllCourses } from "@/hooks";
import { useState } from "react";

// Function to truncate text to a single line
const truncateText = (text: string, maxLength: number = 80) => {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};
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
  const [expandedDescriptions, setExpandedDescriptions] = useState<{ [key: string]: boolean }>({});

  const toggleDescription = (courseId: string) => {
    setExpandedDescriptions(prev => ({
      ...prev,
      [courseId]: !prev[courseId]
    }));
  };

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
        className="mt-6 flex flex-col items-center gap-4"
      >
       <div className="flex flex-col gap-6 w-full mb-10">
      <RadioGroup
        onValueChange={(e) => setSelectedOption(e)}
        className="flex flex-col gap-6"
      >
        {isLoading ? (
          <p>Loading...</p>
        ) : (
          data &&
          data.map((course: any) => (
            <div 
              className={`flex items-start gap-4 w-full p-4 rounded-lg border transition-all duration-200 ${
                course.status === false 
                  ? "bg-gray-50 border-gray-200 opacity-60" 
                  : "bg-white border-gray-200 hover:border-red-300 hover:shadow-sm"
              }`} 
              key={course.id}
            >
              <RadioGroupItem
                value={course.name}
                id={course.name}
                disabled={course.status === false} 
                className={`ring-1 border ring-red-500 mt-1 ${
                  course.status === false ? "opacity-50 cursor-not-allowed" : "border-red-500"
                }`}
              />
              <div className="flex flex-col gap-2 flex-1">
                <Label
                  htmlFor={course.name}
                  className={`font-semibold text-base capitalize ${
                    course.status === false 
                      ? "text-gray-500 select-none cursor-not-allowed" 
                      : "text-gray-900"
                  }`}
                >
                  {course.name}
                </Label>
                {course.description && (
                  <div className="space-y-2">
                    <p className={`text-sm text-gray-600 leading-relaxed ${
                      course.status === false 
                        ? "text-gray-400" 
                        : ""
                    }`}>
                      {expandedDescriptions[course.id] 
                        ? course.description 
                        : truncateText(course.description, 80)
                      }
                    </p>
                    {course.description.length > 80 && (
                      <button
                        type="button"
                        onClick={() => toggleDescription(course.id)}
                        className={`text-xs font-medium underline hover:no-underline ${
                          course.status === false 
                            ? "text-gray-500 hover:text-gray-600" 
                            : "text-red-600 hover:text-red-700"
                        }`}
                      >
                        {expandedDescriptions[course.id] ? "Show Less" : "Show More"}
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </RadioGroup>
    </div>


        <CustomButton
          variant="default"
          disabled={isUpdatingSteps || !selectedOption}
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
    </div>
  );
}
