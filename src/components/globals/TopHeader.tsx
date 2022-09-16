import React from 'react'
import { ArrowRight } from './icons'
import { motion } from 'framer-motion'
import Countdown from 'react-countdown';


const TopHeader = () => {
  return (
    <>
    {/* <div className="hidden  bg-base dark:bg-primary md:flex justify-center items-center h-14">
      <div className=" px-5 text-sm mr-4 font-normal font-secondary text-white ">
        🎉Free: Registration for the cohort VII currently ongoing Apply
        <span className="underline ml-1 text-white10">
          <a href="https://google.com">here</a>
        </span>
      </div>
      <motion.div
        animate={{ x: -10 }}
        transition={{ yoyo: Infinity, duration: 1 }}
        className="hidden md:block "
      >
        <ArrowRight />
      </motion.div>
    </div> */}

    <div>
      <div className="bg-base dark:bg-primary flex p-3 justify-center items-center">
        <div className=" px-5 text-sm mr-4 font-normal font-secondary text-white text-center ">
          🎉Free: Registration for the cohort VIII be live in
          <span className="block text-center  mt-2 text-xl text-white10">
          {/* 1663606804000 -> 
          Timestamp in milliseconds - 1663606804000
          Monday, September 19, 2022 5:00:04 PM GMT+01:00
          */}
          <Countdown date={1663606804000} />
          </span>
          
          </div>
          </div>
    </div>
    </>
  )
}

export default TopHeader
