import HeroSection from "@/components/about/HeroSection";
import MaxWrapper from "@/components/shared/MaxWrapper";

const page = () => {
  return (
    <main className="min-h-screen overflow-x-hidden flex flex-col">
      <MaxWrapper className="flex flex-col w-full">
        <HeroSection />
      </MaxWrapper>
    </main>
  );
};

export default page;
