"use client";

import React, { useEffect, useState, useMemo, useRef } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Country, State } from "country-state-city";
import {
  Loader2,
  MoveRight,
  MoveLeft,
  Globe,
  MapPin,
  CheckCircle2,
} from "lucide-react";
import { toast } from "sonner";
import { useFetchAllCourses } from "@/hooks";
import { unifiedRegistrationSchema } from "@/lib/validators";
import { COURSE_DETAILS } from "@/lib/course-constants";
import { Checkbox } from "@/components/ui/checkbox";
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
import { Label } from "../ui/label";
import CustomButton from "./CustomButton";
import ZKRegistrationModal from "./ZKRegistrationModal";

// Helper function to truncate text
const truncateText = (text: string, maxLength: number = 80) => {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};

interface UnifiedRegistrationFormProps {
  formData: any;
  setFormData: (data: any) => void;
  submitData: (data: any) => void;
  isRegistering: boolean;
  errorMessage: { name?: string; email?: string; github?: string };
}

export default function UnifiedRegistrationForm({
  formData,
  setFormData,
  submitData,
  isRegistering,
  errorMessage,
}: UnifiedRegistrationFormProps) {
  const { data: courses, isLoading: isLoadingCourses } = useFetchAllCourses();
  const [expandedDescriptions, setExpandedDescriptions] = useState<{
    [key: string]: boolean;
  }>({});
  const [showZKModal, setShowZKModal] = useState(false);
  const [countryCode, setCountryCode] = useState<string>("");
  const [hasConsented, setHasConsented] = useState(false);
  const [consentChecked, setConsentChecked] = useState(false);
  
  const formContainerRef = useRef<HTMLDivElement>(null);

  const form = useForm<z.infer<typeof unifiedRegistrationSchema>>({
    resolver: zodResolver(unifiedRegistrationSchema),
    defaultValues: {
      course: formData?.course || "",
      name: formData?.name || "",
      email: formData?.email || "",
      number: formData?.number || "",
      github: formData?.github || "",
      country: formData?.country || "",
      state: formData?.state || "",
      venue: formData?.venue || "",
      gender: formData?.gender || "male",
    },
  });

  const selectedCourseName = form.watch("course");
  const selectedVenue = form.watch("venue");

  const selectedCourseObj = useMemo(() => {
    if (!courses || !selectedCourseName) return null;
    return courses.find((c: any) => c.name === selectedCourseName);
  }, [courses, selectedCourseName]);

  const courseDetail = useMemo(() => {
    if (!selectedCourseName) return null;
    return COURSE_DETAILS[selectedCourseName] || null;
  }, [selectedCourseName]);

  // Reset consent when course changes
  useEffect(() => {
    setHasConsented(false);
    setConsentChecked(false);
    
    // Scroll to top of the form when selecting a new course
    if (selectedCourseName && formContainerRef.current) {
      const topOffset = formContainerRef.current.getBoundingClientRect().top + window.scrollY - 100; // 100px buffer for header
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }
  }, [selectedCourseName]);

  // Sync errorMessage from parent
  useEffect(() => {
    if (errorMessage?.name) {
      form.setError("name", { type: "manual", message: errorMessage.name });
    }
    if (errorMessage?.email) {
      form.setError("email", { type: "manual", message: errorMessage.email });
    }
    if (errorMessage?.github) {
      form.setError("github", { type: "manual", message: errorMessage.github });
    }
  }, [errorMessage, form]);

  const toggleDescription = (courseId: string) => {
    setExpandedDescriptions((prev) => ({
      ...prev,
      [courseId]: !prev[courseId],
    }));
  };

  const isZKCourse = (courseName: string) => {
    const name = courseName.toLowerCase();
    const isZK =
      name.includes("zk") ||
      name.includes("zero knowledge") ||
      name.includes("zero-knowledge");
    const isRust = name.includes("rust");
    return isZK && !isRust;
  };

  const countries = Country.getAllCountries();
  const states = State.getStatesOfCountry(countryCode);

  async function onSubmit(values: z.infer<typeof unifiedRegistrationSchema>) {
    setFormData(values);

    // If ZK course, show modal first
    if (isZKCourse(values.course)) {
      setShowZKModal(true);
    } else {
      submitData(values);
    }
  }

  const proceedWithZK = () => {
    setShowZKModal(false);
    submitData(form.getValues());
  };

  const sortedCourses = useMemo(() => {
    if (!courses) return [];
    return [...courses].sort((a, b) => {
      if (a.status === b.status) return 0;
      return a.status ? -1 : 1;
    });
  }, [courses]);

  const showGitHub = useMemo(() => {
    if (!selectedCourseName) return true;
    return !selectedCourseName.toLowerCase().includes("beginner");
  }, [selectedCourseName]);

  // Define venue options based on course data or default to Online/Onsite
  const venueOptions = useMemo(() => {
    const defaultOptions = [
      {
        id: "online",
        label: "Online",
        icon: Globe,
        description: "Join from anywhere via Google Meet/Discord",
      },
      {
        id: "onsite",
        label: "Onsite",
        icon: MapPin,
        description: "Join us in person at our Lagos hub",
      },
    ];

    if (!selectedCourseObj) return defaultOptions;

    // Explicitly handle Web2 courses based on IDs or names
    const isWeb2Course =
      selectedCourseName.toLowerCase().includes("web2") ||
      [44, 45, 46].includes(selectedCourseObj.id);

    if (isWeb2Course) {
      // For Web2 courses, only allow Online
      return [defaultOptions[0]];
    }

    // For other courses, filter by what's in the venue array if it exists
    if (
      Array.isArray(selectedCourseObj.venue) &&
      selectedCourseObj.venue.length > 0
    ) {
      const availableVenues = selectedCourseObj.venue.map((v: string) =>
        v.toLowerCase(),
      );
      return defaultOptions.filter((option) =>
        availableVenues.includes(option.id),
      );
    }

    return defaultOptions;
  }, [selectedCourseObj, selectedCourseName]);

  // Auto-select venue if only one is available
  useEffect(() => {
    if (venueOptions.length === 1 && selectedCourseName) {
      const currentVenue = form.getValues("venue");
      if (currentVenue !== venueOptions[0].id) {
        form.setValue("venue", venueOptions[0].id);
      }
    }
  }, [venueOptions, form, selectedCourseName]);

  const handleConsentContinue = () => {
    setHasConsented(true);
    // Scroll to top of the form when moving to the personal details step
    if (formContainerRef.current) {
      const topOffset = formContainerRef.current.getBoundingClientRect().top + window.scrollY - 100;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }
  };

  return (
    <div ref={formContainerRef} className="max-w-[750px] w-full px-4 md:px-8 py-8 bg-white dark:bg-secondary/40 rounded-xl shadow-md transition-all duration-500 overflow-hidden">
      <div className="mb-8 border-b pb-4">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Registration
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1 text-sm">
          Join the next cohort of builders at Web3bridge.
        </p>
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          {/* Section 1: Course Selection */}
          {!selectedCourseName && (
            <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-bridgeRed text-white text-xs">
                  1
                </span>
                Select Your Course
              </h2>

              <FormField
                control={form.control}
                name="course"
                render={({ field }) => (
                  <FormItem className="space-y-3">
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                        className="grid grid-cols-1 gap-4"
                      >
                        {isLoadingCourses ? (
                          <div className="flex items-center gap-2 p-4">
                            <Loader2 className="w-4 h-4 animate-spin" />
                            <span>Fetching courses...</span>
                          </div>
                        ) : (
                          sortedCourses.map((course: any) => (
                            <div
                              key={course.id}
                              className={`flex items-start gap-3 p-4 rounded-lg border transition-all cursor-pointer ${
                                course.status === false
                                  ? "bg-gray-50 border-gray-200 opacity-60 grayscale"
                                  : field.value === course.name
                                    ? "bg-red-50/50 border-bridgeRed shadow-[0_0_15px_-5px_rgba(250,1,1,0.2)]"
                                    : "bg-white border-gray-200 hover:border-red-300 hover:bg-red-50/10"
                              }`}
                              onClick={() =>
                                course.status !== false &&
                                field.onChange(course.name)
                              }
                            >
                              <FormControl>
                                <RadioGroupItem
                                  value={course.name}
                                  id={course.name}
                                  disabled={course.status === false}
                                  className="mt-1"
                                />
                              </FormControl>
                              <div className="flex-1">
                                <Label
                                  htmlFor={course.name}
                                  className={`font-bold text-base cursor-pointer flex items-center justify-between ${
                                    course.status === false
                                      ? "text-gray-400"
                                      : "text-gray-900 dark:text-white"
                                  }`}
                                >
                                  <span>{course.name}</span>
                                  {course.status === false && (
                                    <span className="ml-2 text-[10px] bg-gray-200 text-gray-600 px-2 py-0.5 rounded uppercase">
                                      Closed
                                    </span>
                                  )}
                                </Label>
                                {course.description && (
                                  <div className="mt-1">
                                    <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                                      {expandedDescriptions[course.id]
                                        ? course.description
                                        : truncateText(course.description, 95)}
                                    </p>
                                    {course.description.length > 95 && (
                                      <button
                                        type="button"
                                        onClick={(e) => {
                                          e.stopPropagation();
                                          toggleDescription(course.id);
                                        }}
                                        className="text-xs font-semibold text-bridgeRed mt-1 hover:underline"
                                      >
                                        {expandedDescriptions[course.id]
                                          ? "Show Less"
                                          : "Show More"}
                                      </button>
                                    )}
                                  </div>
                                )}
                              </div>
                            </div>
                          ))
                        )}
                      </RadioGroup>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          )}

          {/* New Section: Course Detail & Consent */}
          {selectedCourseName && !hasConsented && courseDetail && (
            <div className="space-y-6 pt-2 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center justify-between mb-4 border-b pb-4 shadow-sm">
                <button
                  type="button"
                  onClick={() => form.setValue("course", "")}
                  className="text-sm font-medium text-gray-500 hover:text-bridgeRed flex items-center gap-1 transition-colors group"
                >
                  <MoveLeft className="w-4 h-4 transition-transform group-hover:-translate-x-1" />{" "}
                  Change Course
                </button>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                    Registration Fee
                  </span>
                  <div className="text-sm font-black text-bridgeRed bg-red-50 border border-red-100 px-3 py-1 rounded-full">
                    {courseDetail.price}
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 dark:bg-gray-900/50 rounded-2xl p-6 md:p-8 border border-gray-100 dark:border-gray-800 shadow-inner">
                <div className="prose prose-sm dark:prose-invert max-w-none">
                  {courseDetail.letter.split("\n").map((line, i) => {
                    const parts = line.split(/(\*\*.*?\*\*)/g);
                    return (
                      <p
                        key={i}
                        className="mb-4 text-gray-700 dark:text-gray-300 font-['Outfit'] leading-relaxed last:mb-0"
                      >
                        {parts.map((part, index) => {
                          if (part.startsWith("**") && part.endsWith("**")) {
                            return (
                              <strong
                                key={index}
                                className="font-bold text-gray-900 dark:text-white"
                              >
                                {part.slice(2, -2)}
                              </strong>
                            );
                          }
                          return part;
                        })}
                      </p>
                    );
                  })}
                </div>
              </div>

              <div className="pt-4 space-y-6">
                <label
                  className={`flex items-start gap-4 p-5 rounded-2xl border-2 transition-all cursor-pointer ${
                    consentChecked
                      ? "bg-red-50/40 border-bridgeRed shadow-md"
                      : "bg-white dark:bg-gray-950 border-gray-100 dark:border-gray-800 hover:border-red-100"
                  }`}
                >
                  <Checkbox
                    id="consent"
                    checked={consentChecked}
                    onCheckedChange={(checked: boolean | "indeterminate") =>
                      setConsentChecked(checked === true)
                    }
                    className="mt-1 w-5 h-5 border-gray-300 data-[state=checked]:bg-bridgeRed data-[state=checked]:border-bridgeRed transition-colors"
                  />
                  <div className="space-y-1 select-none">
                    <span className="text-sm font-bold text-gray-800 dark:text-gray-200 leading-tight">
                      I hereby confirm that I have read and understood perfectly
                      all the details and policies regarding this programme.
                    </span>
                  </div>
                </label>

                <div className="flex justify-center">
                  <CustomButton
                    type="button"
                    onClick={handleConsentContinue}
                    disabled={!consentChecked}
                    className="w-full max-w-[340px] h-14 text-base font-black bg-bridgeRed hover:bg-bridgeRed/90 text-white rounded-full transition-all hover:scale-[1.02] active:scale-[0.98] shadow-xl shadow-bridgeRed/20 disabled:opacity-50 disabled:grayscale disabled:scale-100 uppercase tracking-wide"
                  >
                    Continue to Registration{" "}
                    <MoveRight className="w-5 h-5 ml-2" />
                  </CustomButton>
                </div>
              </div>
            </div>
          )}

          {/* Section 2: Personal Details (Revealed after selection and consent) */}
          {selectedCourseName && hasConsented && (
            <div className="space-y-6 pt-6 font-['Outfit'] animate-in fade-in slide-in-from-top-4 duration-500 fill-mode-forwards">
              <div className="flex items-center justify-between mb-4 border-b pb-4">
                <button
                  type="button"
                  onClick={() => form.setValue("course", "")}
                  className="text-sm font-medium text-gray-500 hover:text-bridgeRed flex items-center gap-1 transition-colors group"
                >
                  <MoveLeft className="w-4 h-4 transition-transform group-hover:-translate-x-1" />{" "}
                  Change Course
                </button>
                <div className="text-sm font-bold text-bridgeRed bg-red-50 border border-red-100 px-3 py-1 rounded-full">
                  {selectedCourseName}
                </div>
              </div>

              <h2 className="text-lg font-semibold flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-bridgeRed text-white text-xs">
                  2
                </span>
                Personal Details
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Full Name</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="John Doe"
                          className="h-12 bg-gray-50/30"
                          {...field}
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
                    <FormItem>
                      <FormLabel>Email Address</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="john@example.com"
                          className="h-12 bg-gray-50/30"
                          {...field}
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
                    <FormItem>
                      <FormLabel>Phone Number</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="+234..."
                          className="h-12 bg-gray-50/30"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {showGitHub && (
                  <FormField
                    control={form.control}
                    name="github"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>GitHub Profile Link</FormLabel>
                        <FormControl>
                          <Input
                            placeholder="https://github.com/username"
                            className="h-12 bg-gray-50/30"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                )}

                {/* Enhanced Venue Selection */}
                <FormField
                  control={form.control}
                  name="venue"
                  render={({ field }) => (
                    <FormItem className="col-span-1 md:col-span-2">
                      <FormLabel className="text-base font-semibold">
                        Preferred Venue
                      </FormLabel>
                      <FormControl>
                        <RadioGroup
                          onValueChange={field.onChange}
                          defaultValue={field.value}
                          className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2"
                        >
                          {venueOptions.map((option) => {
                            const Icon = option.icon;
                            const isSelected = field.value === option.id;
                            return (
                              <div key={option.id}>
                                <RadioGroupItem
                                  value={option.id}
                                  id={`venue-${option.id}`}
                                  className="peer sr-only"
                                />
                                <Label
                                  htmlFor={`venue-${option.id}`}
                                  className={`relative flex flex-col items-center justify-center p-6 rounded-2xl border-2 transition-all cursor-pointer hover:bg-gray-50/50 ${
                                    isSelected
                                      ? "bg-red-50/30 border-bridgeRed shadow-lg shadow-red-500/10"
                                      : "bg-white dark:bg-gray-900 border-gray-100 dark:border-gray-800"
                                  }`}
                                >
                                  <div
                                    className={`p-3 rounded-xl mb-4 ${isSelected ? "bg-bridgeRed text-white" : "bg-gray-100 dark:bg-gray-800 text-gray-500"}`}
                                  >
                                    <Icon className="w-6 h-6" />
                                  </div>
                                  <span
                                    className={`text-base font-bold mb-1 ${isSelected ? "text-bridgeRed" : "text-gray-900 dark:text-white"}`}
                                  >
                                    {option.label}
                                  </span>
                                  <span className="text-xs text-gray-500 text-center max-w-[150px]">
                                    {option.description}
                                  </span>
                                  {isSelected && (
                                    <CheckCircle2 className="absolute top-3 right-3 w-5 h-5 text-bridgeRed" />
                                  )}
                                </Label>
                              </div>
                            );
                          })}
                        </RadioGroup>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="country"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Country</FormLabel>
                      <Select
                        onValueChange={(value) => {
                          field.onChange(value);
                          const selectedCountry = countries.find(
                            (c) => c.name === value,
                          );
                          setCountryCode(selectedCountry?.isoCode || "");
                          form.setValue("state", "");
                        }}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger className="h-12 bg-gray-50/30">
                            <SelectValue placeholder="Select Country" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent className="max-h-[300px]">
                          {countries.map((country) => (
                            <SelectItem
                              key={country.isoCode}
                              value={country.name}
                            >
                              {country.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="state"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>State / Region</FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                        disabled={!countryCode}
                      >
                        <FormControl>
                          <SelectTrigger className="h-12 bg-gray-50/30">
                            <SelectValue
                              placeholder={
                                countryCode
                                  ? "Select State"
                                  : "Select country first"
                              }
                            />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent className="max-h-[300px]">
                          {states.map((state) => (
                            <SelectItem key={state.isoCode} value={state.name}>
                              {state.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="gender"
                  render={({ field }) => (
                    <FormItem className="md:col-span-2">
                      <FormLabel>Gender</FormLabel>
                      <FormControl>
                        <RadioGroup
                          onValueChange={field.onChange}
                          value={field.value}
                          className="flex flex-wrap gap-6 pt-1"
                        >
                          <FormItem className="flex items-center space-x-2 space-y-0">
                            <FormControl>
                              <RadioGroupItem value="male" id="gender-male" className="border-bridgeRed text-bridgeRed" />
                            </FormControl>
                            <Label htmlFor="gender-male" className="font-normal cursor-pointer">
                              Male
                            </Label>
                          </FormItem>
                          <FormItem className="flex items-center space-x-2 space-y-0">
                            <FormControl>
                              <RadioGroupItem value="female" id="gender-female" className="border-bridgeRed text-bridgeRed" />
                            </FormControl>
                            <Label htmlFor="gender-female" className="font-normal cursor-pointer">
                              Female
                            </Label>
                          </FormItem>
                          <FormItem className="flex items-center space-x-2 space-y-0">
                            <FormControl>
                              <RadioGroupItem value="other" id="gender-other" className="border-bridgeRed text-bridgeRed" />
                            </FormControl>
                            <Label htmlFor="gender-other" className="font-normal cursor-pointer">
                              Prefer not to say / Other
                            </Label>
                          </FormItem>
                        </RadioGroup>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="pt-8 flex justify-center animate-in fade-in slide-in-from-top-2 duration-700 delay-200 fill-mode-forwards">
                <CustomButton
                  type="submit"
                  variant="default"
                  disabled={isRegistering}
                  className="w-full max-w-[320px] h-14 text-base font-bold bg-bridgeRed hover:bg-bridgeRed/90 text-white rounded-full transition-all hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-bridgeRed/20 group"
                >
                  {isRegistering ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      Submit Registration{" "}
                      <MoveRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
                    </>
                  )}
                </CustomButton>
              </div>
            </div>
          )}
        </form>
      </Form>

      {/* ZK Registration Modal */}
      <ZKRegistrationModal
        isOpen={showZKModal}
        onClose={() => setShowZKModal(false)}
        onProceed={proceedWithZK}
      />
    </div>
  );
}
