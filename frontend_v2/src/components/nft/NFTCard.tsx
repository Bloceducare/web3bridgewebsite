import Image, { StaticImageData } from 'next/image'
import React from 'react'

export const NFTCard = ({ images, name }: { images: StaticImageData[], name: string }) => {
    return (
        <main className='w-full flex flex-col gap-3'>

            <div className="w-full h-[280px]">
                <Image
                    priority
                    src={images[0]}
                    alt="NFT"
                    className=" w-full h-full" />
            </div>
            <div className='grid grid-cols-3 gap-3'>
                <Image priority src={images[1]} alt="NFT" className="w-full h-full" />
                <Image priority src={images[2]} alt="NFT" className="w-full h-full" />
                <Image priority src={images[3]} alt="NFT" className="w-full h-full" />
            </div>
            <h2 className=' font-medium'>{name}</h2>
            <div className="flex items-center gap-2">
                <Image src={images[4]} alt="logo" className="w-10 h-10" />
                <h4>Web3bridge</h4>
            </div>
        </main>
    )
}
