"use client";

import { JobHighlight } from "@/components/career/jobHighlight";
import { Button } from "@/components/ui/button";
import { dummyJobData } from "@/data/dummyJobDescription";
import { MoveRight } from "lucide-react";
import Image from "next/image";

export default function JobPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const data = dummyJobData.filter((job) => job.id === id).at(0);

  if (!data) {
    return <div className="p-10">Job not found!</div>;
  }

  const {
    title,
    imageUrl,
    companyOverview,
    jobDescription,
    responsibilities,
    jobRequirements,
  } = data;

  return (
    <section className="mt-10 mb-40">
      <div className="px-20 pb-24">
        <Image
          src={imageUrl ? imageUrl : "/career/Announcements.svg"}
          alt="job image"
          width={1280}
          height={400}
        />

        <h1 className="text-center font-semibold text-[#1F1F1F] text-5xl leading-[60px] mt-16 mb-4">
          {title}
        </h1>

        <JobHighlight data={data} />
      </div>

      <div className="bg-[#FFFBF3] py-24 px-52 space-y-10">
        <ItemWrapper title="Company Overview" value={companyOverview} />

        <ItemWrapper title="Job Description" value={jobDescription} />

        <ItemWrapper title="Responsibilities" value={responsibilities} />

        <ItemWrapper title="Job Requirements" value={jobRequirements} />

        <Button variant={"bridgePrimary"}>
          Apply For Postion <MoveRight className="w-5 h-5 ml-2 " />{" "}
        </Button>
      </div>
    </section>
  );
}

function ItemWrapper({
  title,
  value,
}: {
  title: string;
  value: string | string[];
}) {
  return (
    <div className="space-y-4">
      <h2 className="font-semibold text-[32px] text-[#1F1F1F]">{title}</h2>

      {Array.isArray(value) ? (
        <ol>
          {value.map((item) => (
            <li key={item} className="text-[#1C1C1C] text-base">
              {item}
            </li>
          ))}
        </ol>
      ) : (
        <p className="text-[#1C1C1C] text-base">{value}</p>
      )}
    </div>
  );
}
