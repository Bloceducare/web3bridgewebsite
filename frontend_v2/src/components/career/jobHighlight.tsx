import { MoveRight } from "lucide-react";
import { Button } from "../ui/button";
import { JobDescription } from "@/data/dummyJobDescription";

export function JobHighlight({ data }: { data: JobDescription }) {
  const { title, workplaceType, duration, employmentTYpe } = data;
  return (
    <div className="bg-[#FFF7F5] rounded-[36px] py-5 px-10 flex items-center justify-between">
      <ItemWrapper title="Role" value={title} />
      <ItemWrapper title="Workplace Type" value={workplaceType} />
      <ItemWrapper title="Duration" value={duration ? duration : "n/a"} />
      <ItemWrapper title="Employment" value={employmentTYpe} />
      <Button variant={"bridgePrimary"}>
        Apply For Postion <MoveRight className="w-5 h-5 ml-2 " />{" "}
      </Button>
    </div>
  );
}

function ItemWrapper({ title, value }: { title: string; value: string }) {
  return (
    <div className="space-y-6">
      <p className="text-gray-500">{title}</p>
      <p className="text">{value}</p>
    </div>
  );
}
