import HeroSection from "@/components/home/HeroSection";
import SponsorLists from "@/components/home/SponsorLists";
import MaxWrapper from "@/components/shared/MaxWrapper";
import Testimonial from "@/components/home/Testimonial";
import Essence from "@/components/home/Essence";
import Stats from "@/components/home/Stats";
import Web3 from "@/components/home/Web3";
import Web2 from "@/components/home/Web2";
import Banner from "@/components/home/Banner";
import Community from "@/components/home/Community";
import FAQs from "@/components/home/FAQs";

export default function Home() {
  return (
    <main className="min-h-screen overflow-x-hidden flex flex-col">
      <MaxWrapper className="flex flex-col w-full">
        <HeroSection />
      </MaxWrapper>
      <div className="w-full radial-gradient">
        <SponsorLists />
        <MaxWrapper>
          <Testimonial />
        </MaxWrapper>
      </div>
      <MaxWrapper>
        <Stats />
        <Essence />
        <Web3 />
        <Web2 />
      </MaxWrapper>
      <Banner />
      <Community />
      <MaxWrapper className="flex flex-col w-full">
        <FAQs />
      </MaxWrapper>
    </main>
  );
}
