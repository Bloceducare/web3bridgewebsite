import React from 'react'
import { ArrowRight } from './icons'

const TopHeader = () => {
  return (
    <div className="bg-base flex justify-center items-center h-14">
      <div className=" px-5 text-sm mr-4 font-normal font-secondary text-white ">
        🎉Free: Registration for the cohort VII currently ongoing Apply
        <span className="underline ml-1 text-white10">
          <a href="https://google.com">here</a>
        </span>
      </div>
      <div className="hidden md:block">
        <ArrowRight />
      </div>
    </div>
  )
}

export default TopHeader
