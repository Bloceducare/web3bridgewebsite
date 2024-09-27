import { MoveRight } from "lucide-react";
import { Button } from "../ui/button";
import { JobDescription } from "@/data/dummyJobDescription";
import { ApplicationModal } from "./ApplicationModal";

export function JobHighlight({ data }: { data: JobDescription }) {
  const { title, workplaceType, duration, employmentTYpe } = data;
  return (
    <div className="bg-[#FFF7F5] rounded-[36px] py-3 px-4 lg:py-5 lg:px-10 grid grid-cols-2 gap-4 md:gap-0 md:flex items-center justify-between w-full lg:w-9/12 mx-auto">
      <ItemWrapper title="Role" value={title} />
      <ItemWrapper title="Workplace Type" value={workplaceType} />
      <ItemWrapper title="Duration" value={duration ? duration : "n/a"} />
      <ItemWrapper title="Employment" value={employmentTYpe} />

      <ApplicationModal />
      {/* <Button variant={"bridgePrimary"} className="text-xs md:text-sm">
        Apply For Postion <MoveRight className="w-5 h-5 ml-2 " />{" "}
      </Button> */}
    </div>
  );
}

function ItemWrapper({ title, value }: { title: string; value: string }) {
  return (
    <div className="space-y-3 md:space-y-6">
      <p className="text-gray-500 text-sm md:text-base">{title}</p>
      <p className="text-[#1C1C1C] text-sm md:text-base font-semibold">
        {value}
      </p>
    </div>
  );
}
