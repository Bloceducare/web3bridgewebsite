import React from 'react'
import { missionData } from '../Data'

const Mission = () => {
  return (
    <div className="">
      <div className="mt-20 mx-auto  flex justify-center align-center">
        <div className="font-secondary text-4xl text-base90 font-bold">
          <h1 className="flex justify-center align-center dark:text-white20">
            Here is our story
          </h1>
          <div className="mt-10 w-11/12 text-lg text-center font-secondary text-white60  font-medium mx-auto md:w-4/6 xl:w-3/6 md:text-xl">
            Web3bridge is a program created in 2019 to train Web3 developers in
            Africa. We are working on building sustainable Web3 economy in
            Africa through remote and onsite Web3 development training,
            supporting web3 developers and startups, and lowering barriers of
            entry into the Web3 ecosystem.
          </div>
        </div>
      </div>
      {/* Cards */}
      <div className="flex flex-col justify-center items-center mt-24 md:flex-row md:space-x-6 ">
        {missionData.map((data, index) => {
          return (
            <div
              key={index}
              className=" w-4/5 flex mb-10 flex-col justify-center items-center md:w-3/12 "
            >
              <img src={data.icon} alt="card image" />
              <h2 className="font-primary font-bold text-base90 dark:text-white10 text-2xl text-center my-4">
                {data.title}
              </h2>
              <p className="text-center w-10/12 font-primary text-sm text-white60 dark:text-white20 md:w-4/5 ">
                {data.text}
              </p>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Mission
