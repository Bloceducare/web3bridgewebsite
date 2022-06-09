import React from 'react'
import Marquee from 'react-fast-marquee'

const partnerIcons = [
  './google.png',
  './tesla.png',
  './microsoft.png',
  './udemy.png',
  './microsoft.png',
  './tesla.png',
  './google.png',
]

const Partners = () => {
  return (
    <div className="mt-12 w-full flex flex-col    justify-center items-center ">
      <div className=" w-5/6 ">
        <h1 className="mb-6 font-secondary text-base text-center  text-xl font-semibold md:text-4xl ">
          We Collaborate with
          <span className="ml-3 text-primary">
            200+ Leading tech giant companies
          </span>
        </h1>
        <p className="text-center font-primary text-white60 text-xl ">
          At facilisis sed ornare at etiam mattis. Eget turpis in sed feugiat.
          Adipiscing elit egestas id quisque ut tincidunt etiam tincidunt
          nullam. Luctus.
        </p>
      </div>
      <Marquee pauseOnHover speed={50}>
        <div className="flex justify-content items-center">
          {partnerIcons.map((icon, index) => {
            return (
              <div key={index} className="m-10">
                <img src={icon} alt="partner icons" />
              </div>
            )
          })}
        </div>
      </Marquee>
    </div>
  )
}

export default Partners
