'use client'
import Image, { StaticImageData } from "next/image"
import SVGLine from "./SVGLine"
import { cn } from "@/lib/utils"
import { useState } from "react";
import { Fade } from "react-awesome-reveal";

const SVGWrapper = ({ data }: { data: { title: string, text: string, img: StaticImageData }[] }) => {

    const [hoveredElement, setHoveredElement] = useState<number | null>(null);

    return (
        <div className="w-[90%] h-[550px] lg:block hidden relative">
            <SVGLine />

            {
                data.map((item, index) => {
                    return (
                        <div className={cn("absolute cursor-pointer flex flex-col items-center ", {
                            "top-4 left-[100px]": index === 0,
                            "top-4 left-[470px]": index === 1,
                            "top-4 right-[100px]": index === 2,
                            "top-[240px] left-[100px]": index === 3,
                            "top-[240px] left-[470px]": index === 4,
                            "top-[240px] right-[100px]": index === 5,
                            "top-[480px] left-[100px]": index === 6,
                            "top-[480px] left-[470px]": index === 7,
                            "top-[480px] right-[100px]": index === 8
                        })
                        } key={index}
                            onMouseLeave={() => setHoveredElement(null)}
                            onMouseOver={() => setHoveredElement(index)}
                        >
                            <div className="w-[120px] h-[120px]">
                                <Image src={item.img} alt="Techs" className="w-full h-full" />
                            </div>
                            <h4 className="font-light text-base">{item.title}</h4>
                        </div>
                    )
                })
            }

            {hoveredElement !== null && (
                <Fade direction="up" className={cn("absolute w-[400px] h-[200px] flex justify-center items-center transition-all duration-200 backdrop-blur-2xl", {
                    "top-[120px] left-[100px]": hoveredElement === 0,
                    "top-[120px] left-[470px]": hoveredElement === 1,
                    "top-[120px] right-[100px]": hoveredElement === 2,
                    "top-[340px] left-[100px]": hoveredElement === 3,
                    "top-[340px] left-[470px]": hoveredElement === 4,
                    "top-[340px] right-[100px]": hoveredElement === 5,
                    "top-[580px] left-[100px]": hoveredElement === 6,
                    "top-[580px] left-[470px]": hoveredElement === 7,
                    "top-[580px] right-[100px]": hoveredElement === 8
                })}>
                    <div className="w-full h-full p-4 flex items-center rounded-md ring-2 ring-red-200/90 dark:ring-bridgeRed/40 bg-red-100/40 dark:bg-transparent gap-2">
                        <div className="flex flex-col gap-2 flex-1">
                            <h3 className="font-semibold text-lg">{data[hoveredElement].title}</h3>
                            <p className="text-sm">
                                {data[hoveredElement].text}
                            </p>
                            <div className="flex gap-2 items-center">
                                <span className="text-sm px-3 py-2 rounded-2xl bg-red-200/60">Online</span>
                                <span className="text-sm px-3 py-2 bg-gradient-to-b from-red-200 to-orange-100 dark:text-black rounded-2xl">OnSite</span>
                            </div>
                        </div>
                        <div className="flex justify-center items-center w-[30%]">
                            <Image src={data[hoveredElement].img} alt="Techs" className="w-full h-full object-contain" />
                        </div>
                    </div>
                </Fade>
            )}
        </div >
    )
}

export default SVGWrapper