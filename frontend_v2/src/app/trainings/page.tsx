"use client";

import Join from "@/components/shared/Join";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { Building2, Calendar, GraduationCap, MoveRight } from "lucide-react";
import Image from "next/image";
import Pill from "@/components/shared/pill";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useFetchAllCourses, useFetchAllRegistration } from "@/hooks";

// Function to truncate text to a single line
const truncateText = (text: string, maxLength: number = 80) => {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};
import { Skeleton } from "@/components/ui/skeleton";
import { useEffect, useState } from "react";

const details = [
  {
    desc: "Scholarship Placements For Web 3.0 Students",
    icon: GraduationCap,
  },
  {
    desc: "Free Accommodation and feeding for onsite Students",
    icon: Building2,
  },
  {
    desc: "Web3 Community Exposure  and Hackathons  For Students",
    icon: Building2,
  },
];

export default function Trainings() {
  const { isLoading: regLoading, data: regData } = useFetchAllRegistration();
  const { isLoading: courseLoading, data: courseData } = useFetchAllCourses();
  const router = useRouter();
  const [enrichedData, setEnrichedData] = useState<any[]>([]);
  const currentCohort = process.env.NEXT_PUBLIC_CURRENT_COHORT || 'XIV';

  useEffect(() => {
    if (regData && courseData) {
      const enriched = regData
        .filter((registration: any) => {
          // Keep Master Class regardless of cohort
          if (registration.name.toLowerCase().includes('master class')) {
             return true;
           }
          // Only keep current cohort courses
          return registration.cohort === currentCohort;
        })
        .map((registration: any) => {
          // Get course details for this registration
          const courseDetails = registration.courses.map((courseId: number) => {
            return courseData.find((course: any) => course.id === courseId);
          }).filter(Boolean);

          // Create a description from course names and details
          let description = "";
          if (courseDetails.length > 0) {
            // Add course descriptions if available
            const courseDescriptions = courseDetails
              .map((course: any) => course.description)
              .filter(Boolean);
            
            if (courseDescriptions.length > 0) {
              description = courseDescriptions.join(" ");
            } else {
              // If no descriptions, use course names
              const courseNames = courseDetails.map((course: any) => course.name).join(", ");
              description = courseNames;
            }
          } else {
            description = `Join our ${registration.name} to learn Web3 development skills.`;
          }

          return {
            ...registration,
            description,
            courseDetails
          };
        });

              setEnrichedData(enriched);
      }
    }, [regData, courseData]);

  const isLoading = regLoading || courseLoading;

  return (
    <div className="flex flex-col">
      <MaxWrapper className="py-10 md:py-20 lg:py-40 w-full flex flex-col xl:flex-row lg:justify-between gap-4 relative">
        <div className="w-full max-w-full xl:max-w-[754px] text-center flex flex-col items-center justify-center xl:justify-start xl:items-start xl:text-start">
          <Pill text="Web 3.0 Made Easy" />
          <div className="flex flex-col my-2 gap-4">
            <h1 className="text-3xl md:text-4xl lg:text-5xl lg:leading-[1.2] font-semibold text-black">
              Join 2,000+ students Becoming Web3 Developers.
            </h1>
            <p className="w-full max-w-full xl:max-w-[581px] text-sm md:text-base lg:text-xl font-normal text-black">
              We are supporting web3 developers and startups, and lowering
              barriers of entry into the Web3 ecosystem.
            </p>
          </div>

          <div className="w-full aspect-video flex xl:hidden z-10 rounded-[30px] mt-6 mb-3 bg-[#FB8888]/50 p-3">
            <Image
              priority
              src="/trainings/b-3.jpeg"
              alt="banner-img"
              width={536}
              height={536}
              quality={100}
              className="w-full h-full object-cover rounded-[26px]"
            />
          </div>

          <ul className="list-item space-y-2 my-5 md:my-10">
            {details.map((item) => (
              <li key={item.desc} className="flex items-center">
                <item.icon className="w-4 h-4 mr-2 text-red-500" />
                <p className="text-sm md:text-base font-medium text-black">{item.desc}</p>
              </li>
            ))}
          </ul>

          <Button
            onClick={() => router.push("/register")}
            className="h-14 px-6 mt-12 md:mt-16 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-primary hover:bg-transparent">
            Join The next Cohort <MoveRight className="w-5 h-5 ml-2" />
          </Button>
        </div>

        <div className="h-[536px] w-full max-w-[506px] relative hidden xl:flex justify-center mt-20">
          <div className="h-full w-full z-10 rounded-r-none rounded-[48px] bg-[#FB8888]/50 p-3 pr-0">
            <Image
              priority
              src="/trainings/b-3.jpeg"
              alt="banner-img"
              width={536}
              height={536}
              quality={100}
              className="w-full h-full object-cover rounded-[40px] rounded-r-none"
            />
          </div>
          <div className="absolute h-[341px] top-24 -left-36 w-[464px] rounded-r-none rounded-[48px] bg-[#FB8888]/50 p-3 pr-0">
            <Image
              priority
              src="/trainings/b-2.jpeg"
              alt="banner-img"
              width={536}
              height={536}
              quality={100}
              className="w-full h-full object-cover rounded-[40px] rounded-r-none"
            />
          </div>
          <div className="absolute max-w-[376px] w-full h-[250.7px] -top-24 right-0 rounded-r-none rounded-[48px] bg-[#FB8888]/50 p-3 pr-0">
            <Image
              priority
              src="/trainings/b-1.jpeg"
              alt="banner-img"
              width={536}
              height={536}
              quality={100}
              className="w-full h-full object-cover rounded-[40px] rounded-r-none"
            />
          </div>
        </div>
      </MaxWrapper>

      <MaxWrapper>
        {isLoading
          ? Array.from({ length: 3 }).map((_, _key) => (
              <div
                key={_key}
                className="py-10 md:py-20 flex flex-col gap-3 lg:gap-6 items-center justify-center md:max-w-[727px] mx-auto w-full lg:max-w-[926px]">
                <Skeleton className="h-12 w-full max-w-[649px] rounded-3xl"></Skeleton>
                <Skeleton className="w-full max-w-[920px] rounded-2xl aspect-[2]"></Skeleton>
              </div>
            ))
          : enrichedData &&
            enrichedData.map((item: any) => (
              <section
                key={item.id}
                className="py-10 md:py-20 flex flex-col gap-3 lg:gap-6 items-center justify-center md:max-w-[727px] mx-auto w-full lg:max-w-[926px]">
                <h1 className="font-semibold text-xl sm:text-2xl md:text-3xl lg:text-4xl text-center text-black">
                  {item.name}
                </h1>

                <div className="w-full border rounded-lg p-[2px] bg-gradient-to-b from-[#FFB5B5] to-[#FB888842] shadow-2xl transition-transform duration-300 hover:scale-[1.01]">
                  <div className="w-full h-full bg-background p-6 rounded-sm grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="w-full h-full lg:max-w-[416px] flex flex-col justify-between gap-5">
                                             <p className="font-normal text-base sm:text-lg text-black">
                         {truncateText(item.description, 80)}
                       </p>
                       
                       {/* Course Names as Features */}
                       {item.courseDetails && item.courseDetails.length > 0 && (
                         <div className="mt-4">
                           <h3 className="font-semibold text-sm text-gray-700 mb-2">Courses Included:</h3>
                           <div className="flex flex-wrap gap-2">
                             {item.courseDetails.map((course: any) => (
                               <span 
                                 key={course.id} 
                                 className="px-3 py-1 bg-red-50 text-red-600 text-xs font-medium rounded-full border border-red-200"
                               >
                                 {course.name}
                               </span>
                             ))}
                           </div>
                         </div>
                       )}
                     {/*  <p className="flex items-center gap-3 text-base font-semibold">
                       <Calendar className="w-4 h-4" /> 26th August 2024 </p> */}
                      

                      {/* <div className="flex items-center gap-2">
                        {item?.venue.map((venue: string) => (
                          <Pill key={venue} text={venue} />
                        ))}
                      </div> */}

                      <div className="flex flex-col">
                        <div className="flex items-center flex-col md:flex-row gap-4">
                        <Button
                          onClick={() => router.push("/register")}
                          className="bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 h-14 px-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 text-red-500 font-semibold w-full md:w-max"
                          disabled={item.is_open === false}>
                          Register For Training{" "}
                          <MoveRight className="w-5 h-5 ml-2" />
                        </Button>
                        <Button className="h-14 px-6 rounded-full border-2 ring-2 ring-red-200 border-red-100 text-primary bg-[#FB8888]/10 dark:bg-[#FB8888]/5 hover:bg-[#FB8888]/20 hover:dark:bg-[#FB8888]/10 w-full md:w-max">
                          Learn More
                        </Button>

                        </div>
                   
                      </div>

                      <p
                      className={`text-sm font-medium ${
                        item.is_open === false ? "text-red-500" : "text-green-600"
                      }`}
                    >
                      {item.is_open === false ? "Registration Closed" : "Registration Open"}
                    </p>
                    </div>

                  


                    <div className="flex-1 w-full max-w-[424px] mx-auto lg:mx-0 aspect-[1.3] gap-4 mt-4 md:mt-0 relative">
                      {/* <TrainingImages images={item?.images} /> */}
                    </div>
                  </div>
                </div>
              </section>
            ))}
      </MaxWrapper>
      <Join />
    </div>
  );
}

const TrainingImages = ({ images }: { images: any }) => {
  const isMultipleImages = images.length > 2;

  return images.map(({ id, picture }: { id: number; picture: string }) => (
    <div
      key={id}
      className={`rounded-full h-48 w-48 md:w-64 md:h-64 absolute [&:nth-child(1)]:z-10 border-[4px] border-secondary ${
        isMultipleImages
          ? "[&:nth-child(1)]:top-0 [&:nth-child(1)]:left-0 [&:nth-child(3)]:-bottom-7 [&:nth-child(3)]:left-20"
          : "[&:nth-child(1)]:bottom-0 [&:nth-child(1)]:left-5"
      } [&:nth-child(2)]:top-0 [&:nth-child(2)]:right-5`}>
      <Image
        src={picture}
        alt="training"
        className="w-full h-full rounded-full"
        width={500}
        height={500}
      />
    </div>
  ));
};
