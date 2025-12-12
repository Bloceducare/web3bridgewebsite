"use client";

import React from "react";
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
import ZKRegistrationModal from "./ZKRegistrationModal";

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
  const [showZKModal, setShowZKModal] = useState(false);

  const toggleDescription = (courseId: string) => {
    setExpandedDescriptions(prev => ({
      ...prev,
      [courseId]: !prev[courseId]
    }));
  };

  // Helper function to check if a course is ZK-related (strict, excludes Rust)
  const isZKCourse = (courseName: string) => {
    const name = courseName.toLowerCase();
    const isZK = name.includes('zk') || name.includes('zero knowledge') || name.includes('zero-knowledge');
    const isRust = name.includes('rust');
    return isZK && !isRust;
  };

  function onSubmit(e: any) {
    e.preventDefault();
    if (!selectedOption) {
      return toast.error("You need to select a course");
    }
    
    // Check if the selected course is ZK-related
    if (isZKCourse(selectedOption)) {
      setShowZKModal(true);
    } else {
      proceedToNextStep();
    }
  }

  const proceedToNextStep = () => {
    nextStep();
    setFormData({ ...formData, course: selectedOption });
    setShowZKModal(false);
  };

  // Sort courses: open courses first, then closed courses
  const sortedCourses = data ? [...data].sort((a, b) => {
    // If both have same status, maintain original order
    if (a.status === b.status) return 0;
    // Open courses (true) come first, closed courses (false) come last
    return b.status - a.status;
  }) : [];

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
          sortedCourses &&
          sortedCourses.map((course: any, index: number) => {
            // Check if this is the first course (should show "Available Courses" header)
            const isFirstCourse = index === 0;
            // Check if this is the first closed course to add a separator
            const isFirstClosedCourse = !course.status && 
              (index === 0 || sortedCourses[index - 1].status);
            
            return (
              <React.Fragment key={course.id}>
                {/* {isFirstClosedCourse && (
                  <div className="w-full border-t border-gray-300 dark:border-gray-600 my-4">
                    <div className="text-center -mt-3">
                      <span className="bg-white dark:bg-secondary/40 px-3 text-sm text-gray-500 dark:text-gray-400">
                        Currently Closed
                      </span>
                    </div>
                  </div>
                )} */}
                <div 
                  className={`flex items-start gap-4 w-full p-4 rounded-lg border transition-all duration-200 ${
                    course.status === false 
                      ? "bg-gray-50 border-gray-200 opacity-60" 
                      : "bg-white border-gray-200 hover:border-red-300 hover:shadow-sm"
                  }`} 
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
              </React.Fragment>
            );
          })
        )}
      </RadioGroup>
    </div>


        <CustomButton
          type="submit"
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
      
      {/* ZK Registration Modal */}
      <ZKRegistrationModal
        isOpen={showZKModal}
        onClose={() => setShowZKModal(false)}
        onProceed={proceedToNextStep}
      />
    </div>
  );
}
