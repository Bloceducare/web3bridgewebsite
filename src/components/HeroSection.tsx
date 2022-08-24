import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import { images } from '../Data'

const HeroSection = () => {
  const [currentImage, setCurrentImage] = useState<any>(images[0])

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
          <div className="xl:flex w-full md:max-w-xl justify-between">
            {/* <div className="w-full">
              <input
                className="pl-2 py-3 w-full md:w-11/12  border-2 border-white10 mb-5 md:mb-0"
                placeholder="Enter your email address"
              />
            </div> */}
            <div className="">
              <button className="w-full mb-5 bg-primary mr-2 rounded-sm  text-white font-base xl:w-52 py-3 border-2 border-primary">
              <a href="http://nft.web3bridge.com/ " className='capitalize' target="_blank" rel="noopener noreferrer">
              Web3bridge Nft
              </a>
              </button>
            </div>
            <div className="">
              <button className="w-full bg-secondary  rounded-sm  text-secondary font-base xl:w-52 py-3 border-2  dark:text-primary dark:bg-white dark:border-white">
              <a href="https://event.web3bridge.com/" className='capitalize' target="_blank" rel="noopener noreferrer">
              Web3Lagos Conference
              </a>
              </button>
            </div>
          </div>
        </div>
        {/* Hero image */}
        <div className="w-full md:w-6/12  lg:w-4/12 ">
        <Image
                        src={currentImage}
                        alt="Profile"
                        priority={true}
                        width={400}
                        height={400}
                        placeholder="blur"
                        blurDataURL="data:image/jpeg;base64,/9j/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAIAAoDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAhEAACAQMDBQAAAAAAAAAAAAABAgMABAUGIWEREiMxUf/EABUBAQEAAAAAAAAAAAAAAAAAAAMF/8QAGhEAAgIDAAAAAAAAAAAAAAAAAAECEgMRkf/aAAwDAQACEQMRAD8AltJagyeH0AthI5xdrLcNM91BF5pX2HaH9bcfaSXWGaRm knyJckliyjqTzSlT54b6bk+h0R//2Q=="
                    />
        </div>
      </div>
    </div>
  )
}

export default HeroSection
