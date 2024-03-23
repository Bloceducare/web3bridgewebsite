import TeamCard from "./TeamCard";
import { TeamMembers } from "@/lib/utils";

export default function TeamDisplay() {
  return (
    <section className="w-full flex flex-col gap-8 justify-center md:px-4 md:py-20 py-3">
      <h1 className="font-semibold md:text-4xl text-2xl text-center capitalize ">
        Meet Our Amazing Team
      </h1>
      <p className="text-xl font-light text-center">We have a diverse dev team of amazing humans</p>
      <div className="flex flex-wrap gap-8 w-fit mx-auto justify-center">
        {TeamMembers.map((member, index) => (
          <TeamCard
            key={index}
            name={member.name}
            role={member.role}
            image={member.image}
          />
        ))}
      </div>
    </section>
  );
}
