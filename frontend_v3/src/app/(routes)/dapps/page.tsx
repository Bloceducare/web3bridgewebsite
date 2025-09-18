import { DappsSection } from "@/components/dapps/DappsSection";
import HeroSection from "@/components/dapps/HeroSection";
import { HowToUseDappSection } from "@/components/dapps/HowToUseDappSection";
import Join from "@/components/shared/Join";
import MaxWrapper from "@/components/shared/MaxWrapper";

export default function Dapps() {
  return (
    <main className="min-h-screen flex flex-col">
      <MaxWrapper className="flex flex-col w-full">
        {/* Hero section */}
        <HeroSection />
        <DappsSection />
        <HowToUseDappSection />
      </MaxWrapper>
      <Join />
    </main>
  );
}
