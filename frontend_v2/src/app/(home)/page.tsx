import HeroSection from "@/components/home/HeroSection";
import MaxWrapper from "@/components/shared/MaxWrapper";

export default function Home() {
  return <main className="min-h-screen flex flex-col">
    <MaxWrapper className="flex flex-col w-full">
      <HeroSection />
    </MaxWrapper>
  </main>;
}
