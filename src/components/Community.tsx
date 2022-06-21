import Image from 'next/image'
import React from 'react'
import { FaTelegram } from 'react-icons/fa'
import { teamImages } from '../Data'

const Community = () => {
  return (
    <div className="mt-12 w-full flex flex-col justify-center items-center">
      <div className="font-secondary font-medium, text-base90 dark:text-white20 text-4xl mt-20 mb-7">
        Community
      </div>
      <p className="font-secondary text-white60 font-medium text-l text-center md:w-3/5">
        Penatibus sed imperdiet scelerisque duis tristique neque ipsum.
        Pellentesque enim quisque tristique vel leo leo. At parturient habitasse
        viverra elementum odio condimentum. Urna vitae ut.
      </p>
      <div className="mt-14">
        <button className="flex px-3 py-1 items-center border-2 border-white10">
          <FaTelegram color="#D2E5F1" size="1.5rem" />
          <p className="ml-4 text-base dark:text-white20 ">
            Join our Community
          </p>
        </button>
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
