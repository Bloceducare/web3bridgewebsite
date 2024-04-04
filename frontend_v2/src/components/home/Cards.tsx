import { StaticImageData } from "next/image"


const Cards = ({ data }: { data: { title: string, text: string, img: StaticImageData }[] }) => {

    return (
        <div className='w-full grid md:grid-cols-2 gap-4 lg:hidden'>

        </div>
    )
}

export default Cards