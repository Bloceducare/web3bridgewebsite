import TeamCard from "./TeamCard";
import { TeamMembers } from "@/lib/utils";

export default function Documentaries() {
  return (
    <section className="w-full flex flex-col gap-2 lg:gap-6 justify-center md:px-4 md:py-20 py-3 radial-gradient">
      <h1 className="font-semibold md:text-4xl text-2xl text-center capitalize ">
      Documentaries
      </h1>
      <p className="text-md lg:text-xl font-light text-center lg:leading-8">We have amazing stories to tell. Check out our YouTube channel.</p>
      <iframe className="w-full aspect-video mt-4 lg:mt-0 rounded-2xl" src="https://www.youtube.com/embed/vvae4m-GqNg?si=tIOBoKv5t1zONOI0&rel=0 " title="YouTube video player"  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin"
      ></iframe>
    </section>
  );
}
