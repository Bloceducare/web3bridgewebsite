import React, { Fragment } from 'react'
import HeaderImg from '@assets/about-us/about-header-image.svg'
import GroupImg from '../../assets/about-us/group-image.svg'
import Image from 'next/image'
import type { NextPage } from 'next'

type Images = {
  name: string
  role: string
  image: any
}
const About: NextPage = () => {

  return (
    <Fragment>
      <header className="flex flex-wrap w-[100%] lg:w-[80%] items-center justify-around  mt-12 mx-auto">
        <div className="mb-8 md:mb-auto">
          <Image src={HeaderImg} height={326} width={326} />
        </div>

        <div className="w-[80%] md:w-[50%]">
          <h1 className="text-[2rem] font-bold mb-6 text-[#151515] dark:text-[#D0D0D0]">
            Hey! I'm Ayodeji, business developer, Blockchain Educator and
            founder of Web3bridge.
          </h1>
          <p className="text-[#737373]">
            If you've got a couple of minutes I'd love to share the story of how
            web3bridge has grown as a bootstrapped startup. It's been an awesome
            journey and I couldn't have done it without the support of my team
            around me.
          </p>
        </div>
      </header>
      <section className="flex flex-wrap mt-24 mb-12 items-start justify-around  px-1 lg:px-8 ">
        <div className="mb-11 md:mb-auto bg-[#F3F3F3] dark:bg-[#111111] px-8 sm:px-14 py-12 dark:border dark:border-[#444444]">
          <h1 className="text-center dark:text-white border-b border-b-[#A0A0A0] pb-6 px-4">
            OUR STORY IN TO THE WEB 3
          </h1>
          <ul className="text-[#707070] dark:text-[#D0D0D0] text-sm">
            <li className="my-3">
              <p>Problem</p>
            </li>
            <li className="my-3">
              <p>Solution</p>
            </li>
            <li className="my-3">
              <p>Remote developers</p>
            </li>
            <li className="my-3">
              <p>Lagos</p>
            </li>
            <li className="my-3">
              <p>Physical</p>
            </li>
          </ul>
        </div>
        <div className="w-[90%] sm:w-[70%] md:w-[50%]">
          <Image src={GroupImg} className={'w-full'} />
          <h1 className="mb-6 mt-4 font-bold text-2xl text-[#151515] dark:text-[#D0D0D0]">
            Developers dont have to pay so much to learn web 3
          </h1>
          <p className="mb-4 text-[#737373] dark:text-[#D0D0D0]">
            Web3bridge is a program created in 2019 to train Web3 developers in
            Africa. We are working on building sustainable Web3 economy in
            Africa through remote and onsite Web3 development training,
            supporting web3 developers and startups, and lowering barriers of
            entry into the Web3 ecosystem.
          </p>
          <p className="mt-6 text-[#737373] dark:text-[#D0D0D0]">
            And we take care of accomodation, feeding and data expenses for all
            our onsite participants during the program to make it easier for
            them to learn.
          </p>
        </div>
      </section>
      
    </Fragment>
  )
}

export default About
