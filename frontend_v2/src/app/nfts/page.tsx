import { Art } from "@/components/about/Art";
import { Banner } from "@/components/about/Banner";
import HeroSection from "@/components/about/HeroSection";
import NFTDisplays from "@/components/about/NFTDisplays";
import MaxWrapper from "@/components/shared/MaxWrapper";


export default function NFTs() {
    return (<main className="min-h-screen w-full flex flex-col">
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
    </main>)
}