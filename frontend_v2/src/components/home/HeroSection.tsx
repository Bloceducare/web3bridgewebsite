import { MoveRight } from "lucide-react"
import { Button } from "../ui/button"


const HeroSection = () => {
    return (
        <section className="flex items-center justify-center lg:h-[85vh] md:h-[50vh] h-[80vh]  w-full relative overflow-hidden">
            {/* circles */}
            <main className="w-full h-full flex justify-center items-center">
                {/* first circle  */}
                <div className="lg:w-[900px] md:w-[600px] w-[350px] lg:h-[900px] md:h-[600px] h-[350px] bg-transparent md:border-4 border-2 dark:border-2 border-red-100 dark:border-red-500/50 rounded-full flex justify-center items-center">

                    {/* second circle  */}
                    <div className="lg:w-[650px] md:w-[450px] w-[270px] lg:h-[650px] md:h-[450px] h-[270px] bg-red-100/20 dark:bg-transparent md:border-4 border-2 dark:border-2 border-red-100 dark:border-red-500/50 rounded-full flex justify-center items-center">

                        {/* third circle  */}
                        <div className="lg:w-[450px] md:w-[300px] w-[190px] lg:h-[450px] md:h-[300px] h-[190px] bg-red-100/30 dark:bg-bridgeRed/10 border-4 dark:border-2 border-red-100 dark:border-red-500/30 rounded-full flex justify-center items-center"></div>

                    </div>

                </div>
            </main>
            {/* Overlay */}
            <main className="w-full h-full absolute top-0 left-0 flex items-center justify-center">
                <div className="lg:w-[55%] md:w-[60%] w-full flex flex-col gap-4 items-center justify-center">
                    <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">Learn, Build and Network at Web3Bridge</h1>
                    <p className="lg:w-[85%] w-full text-muted-foreground text-center">Start your career in the Blockchain Development industry by receiving training from industry experts through our 16 weeks hands on bootcamp.</p>
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-bridgeRed hover:text-red-100">
                        Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
                    </Button>
                </div>
            </main>

        </section>
    )
}

export default HeroSection