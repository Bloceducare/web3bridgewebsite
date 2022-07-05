import React from 'react'
import { ArrowRight } from './icons'
import { motion } from 'framer-motion'

const TopHeader = () => {
  return (
    <div className="hidden  bg-base dark:bg-primary md:flex justify-center items-center h-14">
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
    </div>
  )
}

export default TopHeader
