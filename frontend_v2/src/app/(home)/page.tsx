import HeroSection from "@/components/home/HeroSection";
import SponsorLists from "@/components/home/SponsorLists";
import MaxWrapper from "@/components/shared/MaxWrapper";
import Image from "next/image";
import cloud from "../../../public/home/cloud.png";
import Testimonial from "@/components/home/Testimonial";
import Counter from "@/components/home/Counter";


export default function Home() {
  return <main className="min-h-screen flex flex-col">
    <MaxWrapper className="flex flex-col w-full">
      <HeroSection />
      <div className="w-full radial-gradient">
        <SponsorLists />
        <Testimonial />
        <Counter />
      </div>
    </MaxWrapper>
  </main>;
}
