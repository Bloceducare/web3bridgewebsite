import Image, { StaticImageData } from "next/image"


const Sponsor = ({ image }: { image: StaticImageData }) => {
    return (
        <div className="px-8 py-3">
            <Image src={image} className="h-14 w-32 aspect-square object-contain" priority alt="Sponsor" />
        </div>
    )
}

export default Sponsor