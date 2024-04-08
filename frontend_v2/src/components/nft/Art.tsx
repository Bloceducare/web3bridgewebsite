import Image from 'next/image'
import React from 'react'
import ArtImage from "../../../public/nfts/art.png"
import { MoveRight } from 'lucide-react'
import { Button } from '../ui/button'

export const Art = () => {
    return (
        <section className='w-full flex flex-col gap-4 justify-center md:px-16 md:py-20 py-3 radial-gradient'>
            <h1 className='font-semibold md:text-4xl text-2xl text-center capitalize '>Explaining Our Art</h1>

            <main className='w-full flex lg:flex-row flex-col-reverse lg:gap-28 gap-10 justify-between items-center py-6'>
                <div className='md:flex-1 w-full flex flex-col gap-4 items-start'>
                    <p className='leading-relaxed text-left'>The art’s major components include the globe, with Africa very pronounced, a growing and fruit-bearing fig tree, and fruits on the tree shown as Web3bridge logo dropping across the globe. Each dropping fruit represents Web3bridge Alumnis that are already in the global ecosystem contributing while the smaller fruits that are yet to form into Web3bridge logo symbolizes devs in training and those that are yet to come out of the program.</p>
                    <div className="mt-6 w-full flex md:flex-row flex-col items-center md:gap-8 gap-4">
                        <Button className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
                            Get Whitelisted <MoveRight className="w-5 h-5 ml-2" />
                        </Button>
                        <Button className="rounded-full px-12 py-6 border-2 ring-4 ring-red-300 dark:ring-red-400 border-none bg-red-500/10 text-bridgeRed hover:bg-transparent">
                            Comfirm Whitelist
                        </Button>
                    </div>
                </div>

                <div className='lg:w-[450px] lg:h-[450px] md:w-[350px] md:h-[350px] w-full h-[350px]'>
                    <Image
                        priority
                        src={ArtImage}
                        alt="Art"
                        className="w-full h-full"
                    />
                </div>
            </main>
        </section>
    )
}