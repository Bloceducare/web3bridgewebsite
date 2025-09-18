"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { allJobOpenings, categories } from "@/data/Career";
import { useRouter } from "next/navigation";
/* eslint-disable react/no-unescaped-entities */

export default function Openings() {
  const [activeCategory, setActiveCategory] = useState("Professionals");
  const [selectedFilter, setSelectedFilter] = useState("All Openings");

  const router = useRouter();

  const toggleFilter = (category: string) => {
    setSelectedFilter(category);
  };

  const filteredJobs = allJobOpenings.filter(
    (job) =>
      (activeCategory === "Professionals"
        ? !job.tags.includes("Internship")
        : job.tags.includes("Internship")) &&
      (selectedFilter === "All Openings" || job.category === selectedFilter)
  );

  return (
    <div className="max-w-6xl mx-auto my-10 p-6">
      <h1 className="text-4xl font-[600] mb-6 text-[#090808] dark:text-white text-center">
        Current Openings
      </h1>

      <div className="flex justify-center mb-8 space-x-4">
        <Button
          onClick={() => setActiveCategory("Professionals")}
          className="rounded-full px-6 py-2 bg-gradient-to-r from-[#FFE9E2] to-[#FFE9E2] text-[#FA0101] hover:bg-[#FF8A76] dark:bg-[#4A4A4A] dark:text-[#FA0101] dark:hover:bg-[#333333]"
        >
          Professionals
        </Button>
        <Button
          variant={
            activeCategory === "Students & Interns" ? "default" : "outline"
          }
          onClick={() => setActiveCategory("Students & Interns")}
          className="rounded-full px-6 py-2 bg-[#F9F9F9] text-black hover:bg-[#F9F9F9] dark:bg-[#4A4A4A] dark:text-white dark:hover:bg-[#333333]"
        >
          Students & Interns
        </Button>
      </div>

      <div className="flex flex-col md:flex-row gap-6">
        <div className="md:w-3/4 space-y-6">
          {filteredJobs.map((job, index) => (
            <Card
              key={index}
              className="bg-[#FFE9E25C] dark:bg-[#3A3A3A] border-0 rounded-[2rem] text-black dark:text-white"
            >
              <CardHeader>
                <CardTitle className="text-2xl font-bold">
                  {job.title}
                </CardTitle>
                <div className="flex space-x-2">
                  {job.tags.map((tag, tagIndex) => (
                    <Badge
                      key={tagIndex}
                      variant="outline"
                      className="bg-[#FFF1EC] dark:bg-[#5A5A5A] rounded-[2rem] p-1 px-3 text-black dark:text-white border-[#FF725E] dark:border-[#FF725E]"
                    >
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardHeader>
              <CardContent>
                <p>{job.description}</p>
              </CardContent>
              <CardFooter className="flex justify-end">
                <Button
                  className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-[#E6272729] dark:border-red-500 bg-red-500/10 dark:bg-red-500/20 text-bridgeRed dark:text-white hover:bg-transparent dark:hover:bg-transparent"
                  onClick={() => router.push(`/career/${job.id}`)}
                >
                  See More
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        <div className="md:w-1/4">
          <div className="bg-[#FFE9E25C] dark:bg-[#3A3A3A] p-0 text-black dark:text-white">
            <div className="py-3">
              <div className="space-y-2">
                {categories.map((category, index) => (
                  <Button
                    key={index}
                    onClick={() => toggleFilter(category.name)}
                    variant={
                      selectedFilter === category.name ? "default" : "outline"
                    }
                    className={`w-full border-0 rounded-none justify-between ${
                      selectedFilter === category.name
                        ? "bg-[#FDE8E1] dark:bg-[#5A5A5A] rounded-[2rem] text-[#090808] dark:text-white hover:bg-transparent dark:hover:bg-transparent"
                        : "bg-[#FFE9E25C] dark:bg-[#3A3A3A] text-black dark:text-white hover:bg-transparent dark:hover:bg-transparent"
                    }`}
                  >
                    <span>{category.name}</span>
                    <span>({category.count})</span>
                  </Button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center mt-8">
        <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 dark:bg-red-500/20 text-bridgeRed dark:text-white hover:bg-transparent dark:hover:bg-transparent">
          Load More
        </Button>
      </div>
    </div>
  );
}
