import HeroSection from "@/components/home/HeroSection";
import SponsorLists from "@/components/home/SponsorLists";
import MaxWrapper from "@/components/shared/MaxWrapper";
import Testimonial from "@/components/home/Testimonial";
import Essence from "@/components/home/Essence";
import Stats from "@/components/home/Stats";


export default function Home() {
  return <main className="min-h-screen flex flex-col">
    <MaxWrapper className="flex flex-col w-full">
      <HeroSection />
      <div className="w-full radial-gradient">
        <SponsorLists />
        <Testimonial />
      </div>
      <Stats />
      <Essence />
    </MaxWrapper>
  </main>;
}
