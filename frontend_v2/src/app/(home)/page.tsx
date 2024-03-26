import HeroSection from "@/components/home/HeroSection";
import SponsorLists from "@/components/home/SponsorLists";
import MaxWrapper from "@/components/shared/MaxWrapper";
import Testimonial from "@/components/home/Testimonial";
import Counter from "@/components/home/Counter";
import Essence from "@/components/home/Essence";


export default function Home() {
  return <main className="min-h-screen flex flex-col">
    <MaxWrapper className="flex flex-col w-full">
      <HeroSection />
      <div className="w-full radial-gradient">
        <SponsorLists />
        <Testimonial />
      </div>
      <Counter />
      <Essence />
    </MaxWrapper>
  </main>;
}
