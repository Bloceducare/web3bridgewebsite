import Image from 'next/image'
import React from 'react'
import BannerImage from "../../../public/nfts/Nft-highlight.jpeg"
import { Button } from '../ui/button'
import { MoveRight } from 'lucide-react'

export const Banner = () => {
    return (
        <section className='w-full h-[500px] relative mb-20 mt-10 before:absolute before:w-full before:h-full before:bg-bridgeRed before:opacity-30 before:z-10'>
            <Image
                priority
                src={BannerImage}
                alt="Banner"
                className="w-full h-full object-cover"
            />
            <main className='w-full h-full absolute z-20 top-0 left-0 flex md:flex-row flex-col-reverse justify-center items-center lg:px-32 pt-10 md:pt-0 px-6 gap-8'>
                <div className=' flex-1 flex flex-col items-start gap-6'>
                    <h3 className='font-medium lg:text-5xl md:text-4xl text-2xl text-left capitalize text-white leading-relaxed'>Blossoming<br className='hidden md:inline-block' /> Web3bridge</h3>
                    <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-bridgeRed  border-red-300 text-white bg-bridgeRed transition-all duration-200 hover:text-bridgeRed hover:bg-white">
                        Mint NFT <MoveRight className="w-5 h-5 ml-2" />
                    </Button>
                </div>
                <div className='flex-1 flex flex-col p-6 rounded-lg gap-2 bg-[#513956]/50 backdrop:blur-xl ring-2 ring-red-300/20 text-background shadow-md shadow-red-200/30'>
                    <h3 className='font-medium text-gray-50 md:text-2xl text-xl'>Major Components</h3>
                    <p className='text-gray-50'>Blossoming Web3bridge is a 4 by 5 feet art drawn on canvass. The art tells the story of Web3bridge grooming developers from Africa and are all over the world literally or remotely contributing to the growth of the blockchain ecosystem.</p>
                </div>
            </main>
        </section>
    )
}