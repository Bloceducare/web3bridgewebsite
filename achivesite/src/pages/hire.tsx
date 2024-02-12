import React, { useState } from 'react'
import Input from '../components/Input'
import { DropDown } from '../components/globals/icons'
import Image from 'next/image'
import HireImage from '../../assets/hire/illustration.svg'
import type { NextPage } from 'next'
import Button from '../components/Button'

const HireUs: NextPage = () => {
  const [dropDown, setDropDown] = useState('')
  const projectOps = ['Defi', 'NFT', "DAO's", 'Others']
  const submitHandler = (e: any) => {
    e.preventDefault()
  }
  return (
    <section className="px-[1rem] md:px-[5rem] py-[5rem]">
      <div className="sm:mb-32 lg:mb-0 ml-5 sm:ml-10 md:ml-[5rem] lg:ml-0">
        <h2 className="dark:text-primary font-bold mb-1">Hire US!!!</h2>
        <h1 className="dark:text-white text-[2rem]">Lets build some magic</h1>
        <h1 className="dark:text-white text-[2rem]">together</h1>
      </div>
      <div className="flex flex-col-reverse sm:flex-row flex-wrap justify-center lg:justify-start items-start w-full mt-8">
        <div className="bg-[#FDFCFC] dark:bg-base flex flex-col items-center w-full sm:w-[80%] lg:w-[50%] px-6 py-[4rem]">
          <form onSubmit={submitHandler}>
            <label className="self-start text-base90 dark:text-white font-bold">
              Full name
            </label>
            <Input type="text" placeholder="Enter your full name" />
            <label className="self-start text-base90 dark:text-white font-bold">
              Email Address
            </label>
            <Input type="email" placeholder="Enter your email address here" />
            <label className="self-start text-base90 dark:text-white font-bold">
              Product Type
            </label>
            <div className="relative text-white10 px-6 py-2 w-full flex-col items-center justify-start border bg-[#0000] border-white10 rounded-md my-4">
              <div
                onClick={() => setDropDown(dropDown === "type" ? "" : "type")}
                className="flex cursor-pointer items-center w-full"
              >
                <p className="mr-auto">Choose Project</p>
                <DropDown />
              </div>
              <div
                className={`flex ${
                  dropDown === "type" ? "h-[6rem] mt-6 " : "h-0 "
                }  flex-col items-start w-full transition-all`}
              >
                {projectOps.map((item, index) => (
                  <button
                    className={`${
                      dropDown === "type" ? "block" : "hidden"
                    } hover:text-primary`}
                    key={index}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>

            <label className="self-start text-base90 dark:text-white font-bold">
              Budget
            </label>
            <Input placeholder="Enter Your Budget" type="text" />
            <label className="self-start text-base90 dark:text-white font-bold">
              Unique Value Proposition (UVP)
            </label>
            <textarea
              className="text-white10 px-6 py-2 w-full h-[10rem] bg-[#0000] border border-white10 rounded-md my-4"
              placeholder="Tell us more about your business idea"
            ></textarea>
            <Button
              clicked={submitHandler}
              content="SEND MESSAGE"
              type="background"
              class="w-full py-3"
              href=""
            />
          </form>
        </div>
        <div className="w-full sm:w-[80%] lg:w-[40%] flex sm:ml-[4rem] h-[20rem] mt-12 lg:mt-0 mb-20 sm:mb-0">
          <Image src={HireImage} />
          <div className="flex flex-col justify-between  h-full ">
            <div className="mt-[1rem]">
              <h1 className="text-base90 dark:text-white10 mb-4">
                Pay us a visit
              </h1>
              <p className="text-white60">
                No. 3 Abadek Avenue Ogunlewe Street, Ikorodu Lagos
              </p>
            </div>
            <div className="">
              <h1 className="text-base90 dark:text-white10 mb-4">
                Beep us on Whatsapp
              </h1>
              <p className="text-white60">Support@web3bridge.com</p>
              <p className="text-white60">+2348 066 482 612</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default HireUs
