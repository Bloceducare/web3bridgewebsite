"use client"
import { useScrollTrigger } from "@/lib/useScrollTrigger";
import { useState } from "react";
import CountUp from "react-countup";


const Stats = () => {
    const [count, setCount] = useState(0);
    const [counterOn, setCounterOn] = useState(false);
    const isScrolled = useScrollTrigger({
        onEnter: () => setCounterOn(true),
        onExit: () => {
            setCounterOn(false);
            setCount(0);
        }
    });

    return (
        <section className="w-full flex md:flex-row flex-col justify-center lg:gap-20 md:gap-12 gap-6 items-center lg:px-12 px-6 md:my-40 my-20">
            <div className="flex flex-col items-center gap-2">
                <h1 className="text-center lg:text-5xl text-4xl font-semibold text-bridgeRed">
                    {isScrolled && <CountUp start={0} end={880} duration={4} delay={0} useEasing={true} />}+
                </h1>
                <p className="text-center text-base">Introduced into blockchain technology</p>
            </div>
            <div className="flex flex-col items-center gap-2">
                <h1 className="text-center lg:text-5xl text-4xl font-semibold text-bridgeRed">
                    {isScrolled && <CountUp start={0} end={1808}
                        duration={4} delay={0} useEasing={true} />}+
                </h1>
                <p className="text-center text-base">Trained in web2.0</p>
            </div>
            <div className="flex flex-col items-center gap-2">
                <h1 className="text-center lg:text-5xl text-4xl font-semibold text-bridgeRed">
                    {isScrolled && <CountUp start={0} end={7}
                        duration={5} delay={0} useEasing={true} />}+
                </h1>
                <p className="text-center text-base">Decentralized apps built</p>
            </div>
        </section>
    )
}

export default Stats