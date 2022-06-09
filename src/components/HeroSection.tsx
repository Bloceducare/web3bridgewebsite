import React from 'react'

const HeroSection = () => {
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="space-y-0 md:space-y-0 w-10/12 flex flex-col-reverse  items-center justify-around mt-10 md:flex-row ">
        <div className="flex flex-col ">
          <h1 className="max-w-xl mt-10 mb-6 text-4xl font-bold text-center md:mt-0 md:text-5xl md:text-left">
            Learn, Build and Network at Web3Bridge
          </h1>
          <p className="max-w-xl mb-20 text-xl text-center text-white60 md:text-left">
            Web3Bridges have top-notch resources, provided by our a poll of
            blockchain experts and a community driven platform
          </p>
          <div className="flex max-w-xl j justify-between justify-center ">
            <div className="w-full">
              <input
                className="pl-2 py-3 w-11/12  border-2 border-white10"
                placeholder="Enter your email address here"
              />
            </div>
            <div className="">
              <button className="bg-primary  text-white font-base w-32 py-3 border-2 border-primary">
                Register
              </button>
            </div>
          </div>
        </div>
        {/* Hero image */}
        <div className="">
          <img src="./heroimage.png" alt="hero image" />
        </div>
      </div>
    </div>
  )
}

export default HeroSection
