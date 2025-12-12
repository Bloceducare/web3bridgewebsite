import HeroSection from "@/components/hub/HeroSection";
import PioneerSection from "@/components/hub/PioneerSection";
import FeaturesSection from "@/components/hub/FeaturesSection";
import InfoSection from "@/components/hub/InfoSection";
import AvailableSpacesSection from "@/components/hub/AvailableSpacesSection";
import LocationSection from "@/components/hub/LocationSection";
import CTASection from "@/components/hub/CTASection";
import MaxWrapper from "@/components/shared/MaxWrapper";

export default function HubPage() {
  return (
    <main className="min-h-screen overflow-x-hidden flex flex-col">
      <MaxWrapper className="flex flex-col w-full">
        <HeroSection />
      </MaxWrapper>
      <PioneerSection />
      <AvailableSpacesSection />
      <FeaturesSection />
      <MaxWrapper className="flex flex-col w-full">
        <InfoSection />
      </MaxWrapper>
      <LocationSection />
      <CTASection />
    </main>
  );
}
