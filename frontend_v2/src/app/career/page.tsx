import ApplicationCTA from "@/components/Career/Apply";
import Benefits from "@/components/Career/Benefits";
import HeroSection from "@/components/Career/HeroSection";
import Openings from "@/components/Career/Openings";
import Testimonial from "@/components/Career/Testimonal";
import MaxWrapper from "@/components/shared/MaxWrapper";

const page = () => {
  return (
    <main className="min-h-screen overflow-x-hidden flex flex-col">
      <MaxWrapper className="flex flex-col w-full">
        <HeroSection />
      </MaxWrapper>
      <Benefits />
      <MaxWrapper className="flex flex-col w-full">
        <Openings />
      </MaxWrapper>
      <Testimonial />
      <ApplicationCTA />
    </main>
  );
};

export default page;
