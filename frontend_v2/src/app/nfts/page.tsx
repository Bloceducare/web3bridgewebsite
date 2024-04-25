import { Art } from "@/components/nft/Art";
import { Banner } from "@/components/nft/Banner";
import HeroSection from "@/components/nft/HeroSection";
import NFTDisplays from "@/components/nft/NFTDisplays";
import { Utility } from "@/components/nft/Utility";
import MaxWrapper from "@/components/shared/MaxWrapper";

export default function NFTs() {
  return (
    <main className="min-h-screen w-full flex flex-col">
      <MaxWrapper className="flex flex-col w-full">
        {/* hero section  */}
        <HeroSection />
        {/* NFTs */}
        <NFTDisplays />
        {/* Explaning our art */}
        <Art />
      </MaxWrapper>
      {/* banner */}
      <Banner />
      <MaxWrapper className="flex flex-col w-full">
        {/* Utility  */}
        <Utility />
      </MaxWrapper>
    </main>
  );
}
