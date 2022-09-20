import React from 'react'
// import Marquee from 'react-fast-marquee'
import { partnerIcons } from 'data'

const Partners = () => {
  return (
    <div className="flex flex-col items-center justify-center w-full mt-24 ">
      <div className="w-5/6 ">
        <h1 className="mb-6 text-base text-xl font-semibold text-center font-secondary dark:text-white10 md:text-4xl ">
          We Collaborate with
          <span className="ml-3 text-primary">
            Leading tech giant companies
          </span>
        </h1>
        <p className="text-xl md:text-center font-primary text-white60 dark:text-white20 ">
          We have a working partnership with the following brands which helps us
          to move our vision forward.
        </p>
      </div>
      {/* <Marquee pauseOnHover speed={50}>
        <div className="flex items-center justify-content">
          {partnerIcons.map((icon, index) => {
            return (
              <div key={index} className="m-10">
                <img src={icon} alt="partner icons" />
              </div>
            )
          })}
        </div>
      </Marquee> */}
      <div className="flex flex-wrap items-center justify-center w-11/12 mt-12 ml-auto ">
        <div className="flex flex-wrap flex-start">
          {partnerIcons.map((icon, index) => {
            return (
              <div
                key={index}
                className={` ${index === 1 ? 'hidden dark:block' : ''} 
                ${index === 2 ? 'block dark:hidden' : ''}
                ${index === 12 ? 'bg-white' : ''} 
                w-12 h-10 my-6 mx-5 md:w-44 md:h-16 md:my-10 md:mx-22 xl:mx-28 `}
              >
                <img src={icon} alt="partner icons" />
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default Partners
