import React from 'react'
import { ArrowRight } from './icons'
import { motion } from 'framer-motion'

const TopHeader = () => {
  return (
    <div className="flex items-center justify-center text-center bg-base dark:bg-primary h-14">
      <div className="px-5 mr-4 text-sm font-normal text-white font-secondary">
         Registration for the cohort VII currently ongoing Apply 🎉
        <span className="ml-1 underline text-white10">
          <a href="https://www.web3bridge.com/cohort-registration" target="_blank" rel="noopener noreferrer">here</a>
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
