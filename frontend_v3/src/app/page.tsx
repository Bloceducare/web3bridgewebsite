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
import WhatWeDo from "@/components/home/WhatWeDo";
import Cohorts from "@/components/home/Cohorts";
import Partners from "@/components/home/Partners";
import Alumni from "@/components/home/Alumni";

export default function Home() {
  return (
    <main className="min-h-screen overflow-x-hidden flex flex-col">
      <HeroSection />
      <Stats />

      {/** <div className="w-full radial-gradient">
        <MaxWrapper>
          <Testimonial />
        </MaxWrapper>
      </div> */}
      <MaxWrapper>

          <WhatWeDo />
          <Cohorts />
        <Partners />


       {/** <Essence />
        <Web3 />
        <Web2 />*/}
      </MaxWrapper>
      <Alumni />
      {/**<Banner />
      <Community /> */}
      <MaxWrapper className="flex flex-col w-full">
        <FAQs />
      </MaxWrapper>
    </main>
  );
}
