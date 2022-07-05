import React, { Fragment } from 'react'
import HeaderImg from '../../assests/about-us/about-header-image.svg'
import GroupImg from '../../assests/about-us/group-image.svg'
import Founder from '../../assests/about-us/founder.png'
import Cofounder from '../../assests/about-us/Cofounder.svg'
import Head from '../../assests/about-us/Head.svg'
import LeadDev from '../../assests/about-us/LeadDev.svg'
import Oke from '../../assests/about-us/oke.png'
import Pelumi from '../../assests/about-us/Pelumi.png'
import Abims from '../../assests/about-us/Abims.png'
import Falilat from '../../assests/about-us/Falilat.png'
import Kevin from '../../assests/about-us/Kevin.png'
import Jerry from '../../assests/about-us/jerry.png'
import Billy from '../../assests/about-us/billy.png'
import Yetunde from '../../assests/about-us/Yetunde.png'
import Ezra from '../../assests/about-us/Ezra.png'
import Marek from '../../assests/about-us/marek.png'
import Image from 'next/image'
import Button from '../components/Button'
import type { NextPage } from 'next'
type Images = {
  name: string
  role: string
  image: any
}
const About: NextPage = () => {
  const images: Images[] = [
    {
      name: 'Awosika Israel Ayodeji',
      role: 'Founder, Program Manger',
      image: Founder,
    },
    {
      name: 'Akinnusotu Temitayo Daniel',
      role: 'Co-founder, Lead Dev/Mentor',
      image: Cofounder,
    },
    {
      name: 'Katangole Allan',
      role: 'Head, Technical Training',
      image: Head,
    },
    {
      name: 'Jeremiah Noah',
      role: 'Lead dev/ Mentor',
      image: LeadDev,
    },
    {
      name: 'Oke Kehinde',
      role: 'Blockchain Developer/ Mentor',
      image: Oke,
    },
    {
      name: 'Fatolu Pelumi',
      role: 'Blockchain Developer/ Mentor',
      image: Pelumi,
    },
    {
      name: 'Abimbola Adebayo',
      role: 'Blockchain Developer/ Mentor',
      image: Abims,
    },
    {
      name: 'Falilat Owolabi',
      role: 'Blockchain Developer/ Mentor',
      image: Falilat,
    },
    {
      name: 'Ademola Kelvin',
      role: 'Blockchain Developer/ Mentor',
      image: Kevin,
    },
    {
      name: 'Michael Jerry',
      role: 'Community/ Social Media Lead',
      image: Jerry,
    },
    {
      name: 'Suleman U. Ezra',
      role: 'Lead Designer',
      image: Ezra,
    },
    {
      name: 'Yetunde Ige',
      role: 'Project Manager',
      image: Yetunde,
    },
    {
      name: 'Marek Laskowski, PhD',
      role:
        'Advisor, Founder Blockchain.lab (York University). Founder Blockchain Hub. Vice Chair, UN/CEFACT (Methodology & Technology)',
      image: Marek,
    },
    {
      name: 'Billy Luedtke',
      role: 'Advisor & Angel investor',
      image: Billy,
    },
  ]
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
      <section className="mt-[10rem] px-12">
        <h1 className="dark:text-[#D0D0D0] text-center mb-28 font-bold text-2xl md:text-[2rem] ml-8 my-12">
          Pioneered By Awesome Team
        </h1>
        <div className=" flex flex-wrap w-full justify-around md:justify-start">
          {images.map((items, index) => {
            return (
              <div
                key={index}
                className=" w-[90%] sm:w-[45%] md:w-[30%] text-center mb-11 sm:mb-24  md:mr-[1.5rem] text-white"
              >
                <Image
                  key={index}
                  src={items?.image}
                  height={400}
                  width={400}
                />
                <h1 className="text-xl text-[#151515] dark:text-white font-bold">
                  {items?.name}
                </h1>
                <p className="text-[#A1A1A1] w-full">{items?.role}</p>
              </div>
            )
          })}
        </div>
      </section>
    </Fragment>
  )
}

export default About
