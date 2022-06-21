import React, { useState, useContext, useEffect } from 'react'
import { ThemeContext } from '../ThemeContext'
import Link from 'next/link'
import Image from 'next/image'
import DarkLogo from '../../../assests/logo-dark.svg'
import LightLogo from '../../../assests/logo-light.svg'
import { DarkModeIcon, LightModeIcon } from './icons'
import { menuItems } from '../../Data'
import { FaTimes } from 'react-icons/fa'

const Navbar = () => {
  const [display, setDisplay] = useState<any>('hidden')
  const [isLight, setIsLight] = useState<boolean>(false)
  const { theme, setTheme } = useContext(ThemeContext)
  useEffect(() => {
    if (theme === 'light') {
      setIsLight(true)
    } else {
      setIsLight(false)
    }
  }, [theme])
  return (
    <>
      <nav className="w-full border-b border-[#D0D0D0] dark:border-0 h-24 flex items-center justify-center dark:bg-base">
        <div className=" w-11/12  flex items-center justify-between md:w-full md:p-4 lg:w-11/12 lg:p-0">
          {/* Logo */}
          {isLight ? (
            <Image src={LightLogo} className="" />
          ) : (
            <Image src={DarkLogo} />
          )}
          {/* Menu Items */}
          <div className="hidden md:space-x-7 lg:space-x-10 md:flex  ">
            {menuItems.map((menuItem, index) => {
              return (
                <div key={index} className="text-base hover:text-primary">
                  <Link href={menuItem.link}>
                    <a className="dark:text-white">{menuItem.menu}</a>
                  </Link>
                </div>
              )
            })}
          </div>
          {/* Buttons */}
          <div className="flex  space-x-6">
            <button className=" hidden lg:block bg-secondary text-primary font-base  lg:px-[1rem] xl:px-[2rem] py-1 border-2 border-primary">
              Sign in
            </button>
            <button className="px-1 py-0 xl:block bg-primary text-white font-base md:px-2 lg:px-[1rem] xl:px-[2rem] md:py-1 border-2 border-primary ">
              Register
            </button>
            {isLight ? (
              <button
                className=""
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              >
                <DarkModeIcon />
              </button>
            ) : (
              <button
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              >
                <LightModeIcon />
              </button>
            )}

            {/* hamburger Menu */}
            <button
              onClick={() => {
                setDisplay((display: any) => !display)
              }}
              id="menu-btn"
              className="block ml-20 hamburger md:hidden focus:outline-none "
            >
              <span className="hamburger-top dark:bg-white"></span>
              <span className="hamburger-middle dark:bg-white"></span>
              <span className="hamburger-bottom dark:bg-white"></span>
            </button>
          </div>
          {/* mobile menu */}
        </div>
        <div className={`${display ? 'hidden' : ''} md:hidden`}>
          <div
            className={`absolute flex flex-col items-center self-end py-8 mt-10 space-y-6 font-bold bg-white sm:w-auto sm:self-center left-6 right-6 drop-shadow-md 
            ${display ? ' ' : 'ease-in-out duration-1000'} `}
          >
            <button
              onClick={() => {
                setDisplay((display: any) => !display)
              }}
              className="ml-auto mr-5 hamburger left-0 focus:outline-none "
            >
              <FaTimes size={20} color="#FA0101" />
            </button>
            {menuItems.map((menuItem, index) => {
              return (
                <div key={index} className=" text-base  hover:text-primary">
                  <Link href={menuItem.link}>
                    <a>{menuItem.menu}</a>
                  </Link>
                </div>
              )
            })}
          </div>
        </div>
      </nav>
    </>
  )
}

export default Navbar
