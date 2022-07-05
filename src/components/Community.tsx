import React from 'react'
import { FaTelegram } from 'react-icons/fa'
import { teamImages } from '../Data'
import { motion } from 'framer-motion'

const Community = () => {
  return (
    <div className="mt-12 w-full flex flex-col justify-center items-center">
      <div className="font-secondary font-medium, text-base90 dark:text-white20 text-4xl mt-20 mb-7">
        Community
      </div>
      <p className="w-11/12 font-secondary text-white60 font-medium text-l md:text-center md:w-3/5">
        Gain access to our ever growing community to connect with brilliant
        minds and get the needed support for your growth.
      </p>
      <div className="mt-14">
        <motion.button
          whileTap={{ scale: 0.3 }}
          className=" px-3 py-1  border-2 border-white10"
        >
          <a
            href="https://t.me/web3bridge"
            target="_blank"
            rel="noreferrer"
            className="flex first-line:items-center "
          >
            <FaTelegram color="#D2E5F1" size="1.8rem" />
            <p className="ml-4 text-base dark:text-white20 ">
              Join our Community
            </p>
          </a>
        </motion.button>
      </div>
      <div className="w-full md:w-11/12 grid gap-2 grid-cols-2  md:grid-cols-6 md:gap-4 mt-14 justify-center items-center px-5">
        {teamImages.map((image, index) => {
          return (
            <div key={index} className=" w-full mx-auto">
              <img className="w-full md:w-72" src={image} alt="team" />
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Community
