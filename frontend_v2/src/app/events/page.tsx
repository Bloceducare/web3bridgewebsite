import HeroSection from "@/components/events/HeroSection";
import MaxWrapper from "@/components/shared/MaxWrapper";


export default function Events() {
    return (
        <main className="min-h-screen flex flex-col">
            <MaxWrapper className="flex flex-col w-full">
                {/* Hero section */}
                <HeroSection />
            </MaxWrapper>
        </main>
    )
}