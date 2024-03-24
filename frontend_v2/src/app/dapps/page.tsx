import HeroSection from "@/components/dapps/HeroSection";
import Join from "@/components/events/Join";
import MaxWrapper from "@/components/shared/MaxWrapper";


export default function Dapps() {
    return (
        <main className="min-h-screen flex flex-col">
            <MaxWrapper className="flex flex-col w-full">
                {/* Hero section */}
            <HeroSection/>
            </MaxWrapper>
            <Join />
        </main>
    )
}