import HeroSection from "@/components/events/HeroSection";
import UpComing from "@/components/events/UpComing";
import Join from "@/components/shared/Join";
import MaxWrapper from "@/components/shared/MaxWrapper";

export default function Events() {
  return (
    <main className="min-h-screen flex flex-col">
      <MaxWrapper className="flex flex-col w-full">
        {/* Hero section */}
        <HeroSection />
        <UpComing />
      </MaxWrapper>
      <Join />
    </main>
  );
}
