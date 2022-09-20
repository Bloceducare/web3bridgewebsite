import React from 'react'
import { missionData } from 'data'

const Mission = () => {
  return (
    <div className="">
      <div className="flex justify-center mx-auto mt-20 align-center">
        <div className="text-4xl font-bold font-secondary text-base90">
          <h1 className="flex justify-center align-center dark:text-white20">
            Here is our story
          </h1>
          <div className="w-11/12 mx-auto mt-10 text-lg font-medium text-center font-secondary text-white60 md:w-4/6 xl:w-3/6 md:text-xl">
            Web3bridge is a program created in 2019 to train Web3 developers in
            Africa. We are working on building sustainable Web3 economy in
            Africa through remote and onsite Web3 development training,
            supporting web3 developers and startups, and lowering barriers of
            entry into the Web3 ecosystem.
          </div>
        </div>
      </div>
      {/* Cards */}
      <div className="flex flex-col items-center justify-center mt-24 md:flex-row md:space-x-6 ">
        {missionData.map((data, index) => {
          return (
            <div
              key={index}
              className="flex flex-col items-center justify-center w-4/5 mb-10  md:w-3/12"
            >
              <img src={data.icon} alt="card image" />
              <h2 className="my-4 text-2xl font-bold text-center font-primary text-base90 dark:text-white10">
                {data.title}
              </h2>
              <p className="w-10/12 text-sm text-center font-primary text-white60 dark:text-white20 md:w-4/5 ">
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
