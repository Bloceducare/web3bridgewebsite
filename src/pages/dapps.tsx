import React, { Fragment } from 'react'
import type { NextPage } from 'next'
import HeroImg from '../../assets/dapps/hero.svg'
import Image from 'next/image'
import Button from '../components/Button'
import FinanceImg from '../../assets/dapps/finance.svg'
import ArtImg from '../../assets/dapps/art.svg'
import GamingImg from '../../assets/dapps/image.svg'
import TechImg from '../../assets/dapps/tech.svg'
import HydroImg from '../../assets/dapps/hydro.png'
import ChainedImg from '../../assets/dapps/chained.png'
import SafeKeepImg from '../../assets/dapps/safekeep.png'

const Dapps: NextPage = () => {
  const workingList = [
    {
      image: HydroImg,
      name: 'HydroSwap',
      desc:
        'Swap your tokens with ease. A community favourite that allows you to trade tokens with folks across the network.',
      buttonContent: 'OPEN HYDROSWAP',
      plate: 'FINANCE',
      link: 'https://www.hydroswap.org/',
    },
    {
      image: ChainedImg,
      name: 'CHAINED THRIFT',
      desc:
        'Chained Thrift is a decentralized finance application built using blockchain technology. Chained Thrift helps its users achieve their financial goals through a decentralized thrift saving scheme.',
      buttonContent: 'Coming soon',
      plate: 'FINANCE',
      link: '/',
    },
    {
      image: SafeKeepImg,
      name: 'SAFEKEEP',
      desc: 'Get your digital assets locked in a sfe protcol and prevent loss.',
      buttonContent: 'Coming soon',
      plate: 'COLLECTILES',
      link: '/',
    },
  ]
  return (
    <Fragment>
      <header className="flex w-full flex-wrap justify-center px-2 sm:px-5 lg:px-[5rem] py-[4rem] lg:py-[1rem] items-center">
        <div className="  w-[90%] md:w-[80%] lg:w-[50%]  lg:mb-0">
          <h2 className="text-primary mb-6">
            DECENTRALIZED APPLICATIONS (DAPPS)
          </h2>
          <h1 className="text-base90 dark:text-white10 text-4xl">
            Web3Bridge build tools and services for people
          </h1>
          <p className="md:w-[70%] text-base90 dark:text-white10 py-8">
            Dapps are a growing movement of applications that use Ethereum to
            disrupt business models or invent new ones.
          </p>
          <div className="flex flex-wrap w-full items-center">
            <Button
              class=" w-full sm:w-auto py-3 px-10 text-xs sm:text-[1rem] mb-8 sm:mb-0"
              type="background"
              content="Explore Dapps"
              // link="dapps"
              href="dapps"
            />
            <Button
              class="w-full sm:w-auto py-3 px-10 text-xs sm:text-[1rem] border-primary text-primary sm:ml-6"
              type="transparent"
              content="Build Software"
              // link=""
              href=""
            />
          </div>
        </div>
        <div className=" justify-center flex w-[100%] lg:w-[45%] xl:w-[35%] mt-8 lg:ml-4">
          <div className="">
            <Image src={HeroImg} alt="hero-image" />
          </div>
        </div>
      </header>
      <section className="mt-12">
        <h1 className="text-base90 dark:text-white10 text-3xl text-center mb-5">
          Explore dapps
        </h1>
        <p className="text-white60 text-sm text-center px-[5rem] lg:px-[20rem] mb-[8rem]">
          A lot of dapps are still experimental, testing the possibilties of
          decentralized networks. But there have been some successful early
          movers in the technology, financial, gaming and collectibles
          categories.
        </p>
        <h1 className="text-2xl mb-8 text-center dark:text-white10">
          Choose Category
        </h1>
        <div className="flex flex-wrap w-[100%] lg:w-[80%] mx-auto mb-[10rem] items-center justify-around text-white10 px-6 sm:px-0">
          <div className="w-full sm:w-auto border hover:border-primary mb-4 lg:mb-0 hover:shadow-[#ffffff15] shadow-md flex items-center rounded-full px-6 py-2">
            <Image src={FinanceImg} /> <p className="ml-4">De Finance</p>
          </div>
          <div className="border w-full sm:w-auto hover:border-primary mb-4 lg:mb-0 hover:shadow-[#ffffff15] shadow-md flex items-center rounded-full px-6 py-2">
            <Image src={ArtImg} /> <p className="ml-4">Art & Collectibles</p>{' '}
          </div>
          <div className="border w-full sm:w-auto hover:border-primary mb-4 lg:mb-0 hover:shadow-[#ffffff15] shadow-md flex items-center rounded-full px-6 py-2">
            <Image src={GamingImg} /> <p className="ml-4">Gaming</p>{' '}
          </div>
          <div className="border w-full sm:w-auto hover:border-primary mb-4 lg:mb-0 hover:shadow-[#ffffff15] shadow-md flex items-center rounded-full px-6 py-2">
            <Image src={TechImg} /> <p className="ml-4">Technology</p>{' '}
          </div>
        </div>
        <div className="mx-8 md:mx-16 sm:border flex flex-wrap items sm:border-white60 px-6 py-8">
          <div className="w-[90%] mx-auto md:w-[65%] mr-auto">
            <h1 className="text-base90 dark:text-white10 mb-4 font-bold text-lg">
              Do you have decentralized app idea?
            </h1>
            <p className="text-white60">
              All products listed on this page are not official endorsements,
              and are provided for informational purposes only. If you want to
              add a product or provide feedback on the policy raise an issue in
              GitHub.
            </p>
          </div>
          <div className="w-[80%] mx-auto mt-[3rem] md:mt-0 md:w-[30%] justify-center flex items-center">
            <Button
              class=" bg-base90 w-[70%] md:w-auto dark:bg-white text-white dark:text-base90 mx-auto px-6 text-sm font-bold py-2 "
              type="transparent"
              content="Suggest Dapp"
              href=""
            />
          </div>
        </div>
      </section>
      <section id="dapps" className="py-20 mt-10 px-6">
        <h1 className="text-3xl mb-16 text-base90 dark:text-white10 font-bold text-center">
          Check out what we are working on
        </h1>
        <div className="flex flex-wrap w-full justify-center lg:justify-between">
          {workingList.map((item, index) => {
            return (
              <div
                key={index}
                className="w-[95%] sm:w-[80%] md:w-[50%] mx-6 lg:mx-0 lg:w-[30%] mb-12 relative h-[37rem] py-4 px-4 border border-[#78787835] dark:border-white60"
              >
                <div className="w-full mx-auto block mb-10">
                  <Image src={item?.image} alt="img" />
                </div>
                <h1 className="text-base90 dark:text-white10 mb-6 font-bold">
                  {item?.name}
                </h1>

                <button className="bg-white block rounded-sm w-auto mb-4">
                  <p
                    className={`text-sm px-2 py-2  ${
                      item?.plate === 'FINANCE'
                        ? 'text-primary'
                        : 'text-[#5C5ACA]'
                    }`}
                  >
                    {item?.plate}
                  </p>
                </button>

                <p className="text-white50 text-base mb-6">{item?.desc}</p>
                <a href={item.link} target="_blank" rel="noreferrer">
                  <Button
                    class=" py-2 font-bold absolute bottom-4 w-[90%]"
                    type="background"
                    content={item?.buttonContent}
                    href=""
                  />
                </a>
              </div>
            )
          })}
        </div>
      </section>
      <section className="my-16 p-[1rem] lg:px-[5rem]">
        <h1 className="text-3xl mb-6 text-base90 dark:text-white10 font-bold text-center">
          How to try a dapp?
        </h1>
        <p className="text-white60 text-center w-[85%] lg:w-[55%] mx-auto">
          To try a dapp, you'll need a wallet and some ETH. A wallet will allow
          you to connect, or log in. And you'll need ETH to pay any transaction
          fees.{' '}
          <span>
            <a className="underline text-[#5C5ACA]" href="/">
              What are transaction fees?
            </a>
          </span>{' '}
        </p>
        <div className="sm:border border-[#CDCDCD] my-24 w-[90%] sm:w-[80%] md:w-full mx-auto flex flex-wrap">
          <div className="w-[100%] mb-10 sm:mb-0 md:w-[33.3%] py-4 px-4 border sm:border-0 md:border-r border-[#CDCDCD]">
            <h1 className="text-base90 dark:text-white10 font-bold">
              1. Get some ETH
            </h1>
            <p className="text-white60 text-sm lg:text-[1rem] py-7">
              Dapp action cost a transaction fee
            </p>
            <Button
              class="text-base90 dark:text-white10 w-full py-4 border border-base90 dark:border-[#D0D0D0]"
              type="transparent"
              content="Get an ETH"
              href=""
            />
          </div>
          <div className="w-[100%] mb-10 sm:mb-0 md:w-[33.3%] py-4 px-4 border sm:border-0 md:border-r border-[#CDCDCD]">
            <h1 className="text-base90 dark:text-white10 font-bold">
              2. Set up wallet
            </h1>
            <p className="text-white60 text-sm lg:text-[1rem] py-7">
              A wallet is your login for dapp
            </p>
            <Button
              class="text-base90 dark:text-white10 w-full py-4 border border-base90 dark:border-[#D0D0D0]"
              type="transparent"
              content="Find Wallet"
              href=""
            />
          </div>
          <div className="w-[100%] md:w-[33.3%] py-4 px-4 border sm:border-0 border-[#CDCDCD]">
            <h1 className="text-base90 dark:text-white10 font-bold">
              3. Ready
            </h1>
            <p className="text-white60 text-sm lg:text-[1rem] py-7">
              Choose a dapp to try out
            </p>
            <Button
              class="text-base90 dark:text-white10 w-full py-4 border border-base90 dark:border-[#D0D0D0]"
              type="transparent"
              content="Choose dapp"
              href=""
            />
          </div>
        </div>
      </section>
    </Fragment>
  )
}

export default Dapps
