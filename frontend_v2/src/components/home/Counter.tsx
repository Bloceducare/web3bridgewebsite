"use client"
import { useState } from "react";
import CountUp from "react-countup";
import ScrollTrigger from "react-scroll-trigger";

const Counter = () => {
    const [counterOn, setCounterOn] = useState(false)
    return (
        <section className="w-full flex md:flex-row flex-col justify-center lg:gap-20 md:gap-12 gap-6 items-center lg:px-12 px-6 md:my-40 my-20">
            <div className="flex flex-col items-center gap-2">
                <ScrollTrigger onEnter={() => setCounterOn(true)} onExit={() => setCounterOn(false)}>
                    <h1 className="text-center lg:text-5xl text-4xl font-semibold text-bridgeRed">
                        {counterOn && <CountUp start={0} end={880}
                            duration={2} delay={0} useEasing={true} />}+
                    </h1>
                </ScrollTrigger>
                <p className="text-center text-base">Introduced into blockchain technology</p>
            </div>
            <div className="flex flex-col items-center gap-2">
                <ScrollTrigger onEnter={() => setCounterOn(true)} onExit={() => setCounterOn(false)}>
                    <h1 className="text-center lg:text-5xl text-4xl font-semibold text-bridgeRed">
                        {counterOn && <CountUp start={0} end={1808}
                            duration={2} delay={0} useEasing={true} />}+</h1>
                </ScrollTrigger>
                <p className="text-center text-base">Trained in web2.0</p>
            </div>
            <div className="flex flex-col items-center gap-2">
                <ScrollTrigger onEnter={() => setCounterOn(true)} onExit={() => setCounterOn(false)}>
                    <h1 className="text-center lg:text-5xl text-4xl font-semibold text-bridgeRed">
                        {counterOn && <CountUp start={0} end={7}
                            duration={2} delay={0} useEasing={true} />}+
                    </h1>
                </ScrollTrigger>
                <p className="text-center text-base">Decentralized apps built</p>
            </div>
        </section>
    )
}

export default Counter