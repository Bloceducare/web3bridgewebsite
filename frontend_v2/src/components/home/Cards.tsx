'use client'
import Image, { StaticImageData } from "next/image"
import { Slide } from "react-awesome-reveal"


const Cards = ({ data }: { data: { title: string, text: string, img: StaticImageData }[] }) => {

    return (
        <div className='w-full grid md:grid-cols-2 gap-6 lg:hidden'>
            {
                data.map((item, index) => (
                    <Slide key={index} direction={index % 2 === 0 ? "left" : "right"} className="w-full">
                        <div className="w-full p-4 flex items-center rounded-md ring-2 ring-red-200/90 dark:ring-bridgeRed/40 bg-red-100/40 dark:bg-transparent gap-2">
                            <div className="flex flex-col gap-2 flex-1">
                                <h3 className="font-semibold text-lg">{item.title}</h3>
                                <p className=" text-sm">{item.text}</p>
                                <div className="flex gap-2 items-center">
                                    <span className="text-sm px-3 py-2 rounded-2xl bg-red-200/60">Online</span>
                                    <span className="text-sm px-3 py-2 bg-gradient-to-b from-red-200 to-orange-100 dark:text-black rounded-2xl">OnSite</span>
                                </div>
                            </div>
                            <div className="flex justify-center items-center w-[30%]">
                                <Image src={item.img} alt="Techs" className="w-full h-full object-contain" />
                            </div>
                        </div>
                    </Slide>
                ))
            }

        </div>
    )
}

export default Cards