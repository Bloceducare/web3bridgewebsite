import Image, { StaticImageData } from "next/image"
import { Button } from "../ui/button"


const EventCard = ({ image, text }: { image: StaticImageData, text: string }) => {
    return (
        <div className="w-full flex flex-col items-start md:gap-3 gap-4">
            <div className="w-full h-[280px]">
                <Image
                    priority
                    src={image}
                    alt="NFT"
                    className=" w-full h-full" />
            </div>
            <p>{text}</p>
            <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-400 border-none bg-red-500/10 text-bridgeRed hover:bg-transparent">
                Learn More
            </Button>
        </div>
    )
}

export default EventCard