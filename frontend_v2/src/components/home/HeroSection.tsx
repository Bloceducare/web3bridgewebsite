import { MoveRight } from "lucide-react"
import { Button } from "../ui/button"


const HeroSection = () => {
    return (
        <section className="flex items-center justify-center lg:h-[85vh] md:h-[50vh] h-[80vh]  w-full relative">
            <div className="lg:w-[55%] md:w-[60%] w-full flex flex-col gap-4 items-center justify-center">
                <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">Learn, Build and Network at Web3Bridge</h1>
                <p className="lg:w-[85%] w-full text-muted-foreground text-center">Start your career in the Blockchain Development industry by receiving training from industry experts through our 16 weeks hands on bootcamp.</p>
                <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-bridgeRed hover:text-red-100">
                    Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
                </Button>
            </div>
        </section>
    )
}

export default HeroSection