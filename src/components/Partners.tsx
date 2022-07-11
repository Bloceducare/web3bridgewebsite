import React from 'react'
// import Marquee from 'react-fast-marquee'
import { partnerIcons } from '../Data'

const Partners = () => {
  return (
    <div className="mt-24 w-full flex flex-col justify-center items-center ">
      <div className=" w-5/6 ">
        <h1 className="mb-6 font-secondary text-base dark:text-white10 text-center  text-xl font-semibold md:text-4xl ">
          We Collaborate with
          <span className="ml-3 text-primary">
            Leading tech giant companies
          </span>
        </h1>
        <p className="md:text-center font-primary text-white60 dark:text-white20 text-xl ">
          We have a working partnership with the following brands which helps us
          to move our vision forward.
        </p>
      </div>
      {/* <Marquee pauseOnHover speed={50}>
        <div className="flex justify-content items-center">
          {partnerIcons.map((icon, index) => {
            return (
              <div key={index} className="m-10">
                <img src={icon} alt="partner icons" />
              </div>
            )
          })}
        </div>
      </Marquee> */}
      <div className="mt-12 w-11/12  justify-center items-center flex flex-wrap ml-auto ">
        <div className="flex flex-wrap  flex-start">
          {partnerIcons.map((icon, index) => {
            return (
              <div
                key={index}
                className={` ${index === 1 ? 'hidden dark:block' : ''} 
                ${index === 2 ? 'block dark:hidden' : ''} 
                w-12 h-10 my-6 mx-5 md:w-44 md:h-16 md:my-10 md:mx-22 xl:mx-28`}
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
