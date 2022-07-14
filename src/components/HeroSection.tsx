import React, { useState, useEffect } from 'react'
import { images } from '../Data'

const HeroSection = () => {
  const [currentImage, setCurrentImage] = useState<any>(null)

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentImage(images[Math.floor(Math.random() * images.length)])
    }, 1000)

    return () => clearInterval(intervalId)
  }, [])

  return (
    <div className="w-full flex flex-col items-center justify-center">
      <div className="w-11/12 md:w-10/12 flex flex-col-reverse items-center justify-between mt-10 md:mt-20 md:flex-row gap-20">
        <div className="w-11/12 md:w-6/12  lg:w-4/12 flex flex-col ">
          <h1 className="w-full mt-10 mb-6 text-2xl font-bold text-center dark:text-white20 md:mt-0 lg:text-4xl md:text-left">
            Learn, Build and Network at Web3Bridge
          </h1>
          <p className="w-full mb-16 text-xl text-white60">
            Get the right headstart to launch your career in the Blockchain
            Development industry by receiving training from industry experts
            through our 16 weeks hands on bootcamp.
          </p>
          <div className="md:flex w-full md:max-w-xl justify-between">
            {/* <div className="w-full">
              <input
                className="pl-2 py-3 w-full md:w-11/12  border-2 border-white10 mb-5 md:mb-0"
                placeholder="Enter your email address"
              />
            </div> */}
            <div className="">
              <button className="w-full bg-primary  rounded-sm  text-white font-base md:w-32 py-3 border-2 border-primary">
              <a href="https://forms.gle/pc8d31R99fFp4Dzu5" className='capitalize' target="_blank" rel="noopener noreferrer">
                Join wait list
              </a>
              </button>
            </div>
          </div>
        </div>
        {/* Hero image */}
        <div className="w-full md:w-6/12  lg:w-4/12 ">
          <img className="w-[100%]" src={currentImage} alt="hero image" />
        </div>
      </div>
    </div>
  )
}

export default HeroSection
