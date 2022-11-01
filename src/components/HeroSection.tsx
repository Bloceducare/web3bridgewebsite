import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import { images, blurUrl } from 'data'
import Link from 'next/link'

const HeroSection = () => {
  const [currentImage, setCurrentImage] = useState<any>(images[0])

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentImage(images[Math.floor(Math.random() * images.length)])
    }, 1000)

    return () => clearInterval(intervalId)
  }, [])

  return (
    <div className="flex flex-col items-center justify-center w-full">
      <div className="flex flex-col-reverse items-center justify-between w-11/12 gap-20 mt-10 md:w-10/12 md:mt-20 md:flex-row">
        <div className="flex flex-col w-11/12 md:w-6/12 lg:w-4/12 ">
          <h1 className="w-full mt-10 mb-6 text-2xl font-bold text-center dark:text-white20 md:mt-0 lg:text-4xl md:text-left">
            Learn, Build and Network at Web3Bridge
          </h1>
          <p className="w-full mb-16 text-xl text-white60">
            Get the right headstart to launch your career in the Blockchain
            Development industry by receiving training from industry experts
            through our 16 weeks hands on bootcamp.
          </p>
          <div className="justify-between w-full xl:flex md:max-w-xl">
            {/* <div className="w-full">
              <input
                className="w-full py-3 pl-2 mb-5 border-2 md:w-11/12 border-white10 md:mb-0"
                placeholder="Enter your email address"
              />
            </div> */}
            <div className="">
              <button className="w-full py-3 mb-5 mr-2 text-white border-2 rounded-sm bg-primary font-base xl:w-52 border-primary">
              <a href="http://nft.web3bridge.com/ " className='capitalize' target="_blank" rel="noopener noreferrer">
              Web3bridge Nft
              </a>
              </button>
            </div>
            {/* <div className= "w-full py-3 text-center capitalize border-2 rounded-sm bg-secondary text-secondary font-base xl:w-52 dark:text-primary dark:bg-white dark:border-white">
              <Link href="/cohort-registration">
          
              
                Cohort VIII Registration
              
              </Link>
              
            </div> */}
          </div>
        </div>
        {/* Hero image */}
        <div className="w-full md:w-6/12 lg:w-4/12 ">
        <Image
                        src={currentImage}
                        alt="Profile"
                        priority={true}
                        width={400}
                        height={400}
                        placeholder="blur"
                        blurDataURL={blurUrl}
                    />
        </div>
      </div>
    </div>
  )
}

export default HeroSection
