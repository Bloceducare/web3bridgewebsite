import TeamCard from "./TeamCard";
import { TeamMembers } from "@/lib/utils";

export default function TeamDisplay() {
  return (
    <section className="w-full flex flex-col gap-2 lg:gap-6 justify-center py-10 md:px-4 md:py-20 radial-gradient ">
      <h1 className="font-semibold md:text-4xl text-2xl text-center capitalize">
        Meet Our Amazing Team
      </h1>
      <p className="text-md lg:text-xl font-light text-center">We have a diverse dev team of really amazing people</p>
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
