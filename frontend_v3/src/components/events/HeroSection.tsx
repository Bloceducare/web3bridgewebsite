import { Calendar, MapPin, MoveRight } from "lucide-react"
import { Button } from "../ui/button"
import dynamic from "next/dynamic";
import Image from "next/image";
const CountDown = dynamic(() => import("@/components/events/CountDown"), {
    ssr: false,
});
import HeroImg from "../../../public/events/1.png";
import shape1 from "../../../public/events/2.png";
import shape2 from "../../../public/events/3.png";
import shape3 from "../../../public/events/4.png";
import shape4 from "../../../public/events/5.png";

const HeroSection = () => {
    return (
        <section className="grid md:grid-cols-2 lg:h-[85vh] md:h-[60vh] h-auto pt-12 md:pt-0 w-full relative gap-10 md:gap-0">
            {/* text */}
            <div className="w-full flex flex-col justify-center items-center md:items-start md:gap-3 gap-4 lg:px-10 md:px-6 px-2">
                <h1 className="font-semibold leading-tight lg:text-5xl md:text-4xl text-center md:text-start text-3xl">The Web3 Lagos Conference</h1>
                <CountDown targetDate={`2024-09-05T00:00:00`} />
                <h3 className="text-foreground font-medium text-2xl">Happening live at</h3>
                <p className="flex gap-2 items-center text-muted-foreground">
                    <MapPin className="w-5 h-5" />
                    The Zone, Gbagada, Lagos State.</p>
                <p className="flex gap-2 items-center text-muted-foreground">
                    <Calendar className="w-5 h-5" />
                    5th - 7th, September 2024</p>
                <div className="mt-4 hidden md:flex lg:flex-row md:flex-col items-center lg:gap-8 gap-4">
                    <a href="https://event.web3bridge.com" className="">
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
                        Register for Event <MoveRight className="w-5 h-5 ml-2 " />
                    </Button>
                    </a>
                 
                 <a href="https://forms.gle/YGqRUT93fE6qA2jK7" className="">
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-400 border-none bg-red-500/10 text-bridgeRed hover:bg-transparent">
                        Volunteer
                    </Button>
                    </a>
                </div>
            </div>
            {/* image */}
            <div className="w-full md:h-full flex flex-col md:flex-row md:justify-end md:items-end items-center justify-center gap-5 md:gap-0">
                <div className="w-[80%] h-[85%] relative md:before:w-[85%] before:w-full lg:before:h-full md:before:h-[70%] before:h-full before:border-2 before:border-bridgeRed/50 before:absolute md:before:-top-8 before:-top-4 md:before:-left-2 before:-left-4 before:-z-10 before:rounded-lg">
                    <Image src={HeroImg} alt="image" className="w-full lg:h-full md:h-auto h-full lg:object-contain md:object-fill object-contain" priority />
                </div>

                <div className="my-4 md:hidden flex flex-col items-center gap-6">
                <a href="https://event.web3bridge.com" className="">
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
                        Register for Event <MoveRight className="w-5 h-5 ml-2 " />
                    </Button>
                    </a>
                    <a href="https://forms.gle/YGqRUT93fE6qA2jK7" className="">
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-400 border-none bg-red-500/10 text-bridgeRed hover:bg-transparent">
            Volunteer
                    </Button>
                    </a>
                </div>
            </div>

            {/* shapes */}
            <Image src={shape1} alt="shape" className="absolute top-3 md:right-[15%] right-1 object-contain w-6 h-6" />
            <Image src={shape2} alt="shape" className="absolute md:top-[20%] top-[35%] md:right-[46%] right-3 object-contain w-6 h-6" />
            <Image src={shape3} alt="shape" className="absolute md:top-[3%] top-0 left-[30%] object-contain w-6 h-6" />
            <Image src={shape4} alt="shape" className="absolute top-[5%] md:left-10 left-0 object-contain w-6 h-6" />
        </section>
    )
}

export default HeroSection