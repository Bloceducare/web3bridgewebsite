import ApplicationCTA from "@/components/career/Apply";
import Benefits from "@/components/career/Benefits";
import HeroSection from "@/components/career/HeroSection";
import Openings from "@/components/career/Openings";
import Testimonial from "@/components/career/Testimonal";
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
