import React, { Fragment } from 'react'
import Image from 'next/image'
import HeaderImg from '../../assets/alumni/alumnihero.png'
import GroupImg from '../../assets/alumni/group-image.svg'
import Button from '../components/Button'
import type { NextPage } from 'next'
import John from '../../assets/alumni/john.png'
import Blessing from '../../assets/alumni/blessing.png'
import Emma from '../../assets/alumni/emma.png'

const Alumni: NextPage = () => {
  return (
    <Fragment>
      <header className="flex flex-wrap w-full justify-center pt-10 px-2 lg:px-16 items-center">
        <div className=" w-[90%] md:w-[80%] lg:w-[50%] px-1 sm:px-4 lg:px-16">
          <h2 className="text-[#FA0101] text-sm lg:text-[1rem] ">
            JOIN OUR ALUMNI COMMUNITY
          </h2>
          <h1 className=" dark:text-[#D0D0D0] text-xl lg:text-3xl font-bold py-8 md:w-[70%]">
            Welcome to Web3Bridge Alumni Community Hub
          </h1>
          <p className="text-[#737373] md:w-[70%]">
            The community is home to hundreds of thousands of developers,
            technologists, and enthusiasts. People who have graduated our
            cohort, feel free to mingle please.
          </p>
        </div>
        <div className=" w-[100%] flex justify-center lg:w-[45%] mx-auto mt-10 lg:mt-0 ">
          <Image src={HeaderImg} />
        </div>
      </header>
      <section className="sm:text-center mt-[6rem] px-11 lg:px-40">
        <h1 className="dark:text-[#D0D0D0] text-xl sm:text-3xl mb-6 font-bold">
          Cohort VI officially end, the bumpy ride begins
        </h1>
        <p className="mb-20 mx-auto text-[#737373] w-full sm:w-[80%] md:w-[50%] text-sm sm:text-[1rem]">
          Participants of our Web3Bridge program will be participating in Catch
          the flag; where they will be hacking a smart contract with rewards.
        </p>
        <Image src={GroupImg} />
        <div className="w-full flex justify-center mt-4">
          <button className="bg-[#FA0101] mx-1  h-4 w-4 rounded-full cursor-pointer"></button>
          <button className="bg-[#FEE0E0] mx-1 h-4 w-4 rounded-full cursor-pointer"></button>
          <button className="bg-[#FEE0E0] mx-1 h-4 w-4 rounded-full cursor-pointer"></button>
          <button className="bg-[#FEE0E0] mx-1 h-4 w-4 rounded-full cursor-pointer"></button>
        </div>
      </section>
      <section className="mt-32 sm:text-center px-6 sm:px-12">
        <h1 className="dark:text-[#D0D0D0] px-4 mb-4 text-3xl text-bold">
          Past Mentees of our cohorts
        </h1>
        <h2 className="text-[#737373] px-4 mb-24">
          Take a sneak peak at our amazing students who have gone through our
          trainings to become world-class Blockchain Developers.
        </h2>
        <div className="flex flex-wrap items-start justify-around ">
          <div className="text-center w-[90%] sm:w-[70%] mb-12 md:w-[30%]">
            <Image src={John} />
            <h1 className="font-bold mb-2 dark:text-[#D0D0D0]">John Odey</h1>
            <p className="text-[#A1A1A1] text-sm">Web3 Cohort V</p>
            <p className="text-[#A1A1A1] text-sm">Student(2021)</p>
          </div>
          <div className="text-center w-[90%] sm:w-[70%] mb-12 md:w-[30%]">
            <Image src={Blessing} />
            <h1 className="font-bold mb-2 dark:text-[#D0D0D0]">
              Blessing Emah
            </h1>
            <p className="text-[#A1A1A1] text-sm">Web3 Cohort VI</p>
            <p className="text-[#A1A1A1] text-sm"> Student(2020)</p>
          </div>
          <div className="text-center w-[90%] sm:w-[70%] mb-12 md:w-[30%]">
            <Image src={Emma} />
            <h1 className="font-bold mb-2 dark:text-[#D0D0D0]">
              Emmanuel Chinatuka
            </h1>
            <p className="text-[#A1A1A1] text-sm">Cohort IV, Web 2</p>
            <p className="text-[#A1A1A1] text-sm"> Mentee (2021)</p>
          </div>
        </div>
        <Button
          href=""
          class="mx-auto block px-10 py-1 mt-12 dark:text-[#D0D0D0] border-[#151515] dark:border-[#D0D0D0]"
          type="transparent"
          content="View More"
        />
      </section>
      <section className="bg-[#F3F3F3] dark:bg-[#151515] sm:text-center px-10 sm:px-0 py-14 mt-24">
        <h1 className="text-3xl font-bold mb-8 dark:text-[#D0D0D0]">
          Join our Alumni Club
        </h1>
        <p className="sm:w-[50%] mx-auto mb-12 text-[#737373]">
          You can also join our Alumni club by participating in our cohort based
          trainings for Web3 and Web2.
        </p>
        <Button
          href=""
          class="text-white bg-[#151515] dark:bg-[#FA0101] dark:border-[#FA0101] px-6 py-2"
          type="transparent"
          content="Become a member"
        />
      </section>
    </Fragment>
  )
}

export default Alumni
