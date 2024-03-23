import Documentaries from "@/components/about/Documentaries";
import  HeroSection  from "@/components/about/HeroSection";
import StoryDisplay from "@/components/about/StoryDisplay";
import TeamDisplay from "@/components/about/TeamDisplay";
import MaxWrapper from "@/components/shared/MaxWrapper";

export default function About() {
    return <main className="min-h-screen flex flex-col">
        <MaxWrapper className="flex flex-col w-full">
            {/* Hero section */}
            <HeroSection />
            <StoryDisplay/>
            <TeamDisplay/>
            <Documentaries/>
        </MaxWrapper>
    </main>;
}