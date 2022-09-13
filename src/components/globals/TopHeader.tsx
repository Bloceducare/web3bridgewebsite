import React from 'react'
import { ArrowRight } from './icons'
import { motion } from 'framer-motion'
import Countdown from 'react-countdown';

// days to miliseconds
const dayToCountdown = 5
const daysToMiliseconds = (days: number) => days * 24 * 60 * 60 * 1000 + Date.now()  + 61200000

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
          🎉Free: Registration for the cohort VIII be live soon
          <span className="block text-center  mt-2 text-xl text-white10">
          <Countdown date={daysToMiliseconds(dayToCountdown)} />
          </span>
          
          </div>
          </div>
    </div>
    </>
  )
}

export default TopHeader
