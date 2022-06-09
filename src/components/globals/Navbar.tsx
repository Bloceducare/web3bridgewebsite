import React, { useState } from 'react'
// import { useTheme } from 'next-theme'
import Link from 'next/link'
import { ModeIcon } from './icons'

const menuItems = [
  {
    menu: 'Home',
    link: 'www.google.com',
  },
  {
    menu: 'About Us',
    link: 'www.google.com',
  },
  {
    menu: 'Cohorts',
    link: 'www.google.com',
  },
  {
    menu: 'dApps',
    link: 'www.google.com',
  },
  {
    menu: 'Alumni',
    link: 'www.google.com',
  },
  {
    menu: 'Hire us',
    link: 'www.google.com',
  },
]

const Navbar = () => {
  const [display, setDisplay] = useState<any>('hidden')

  //   const { systemTheme, theme, setTheme } = useTheme()
  //   const currentThemeChanger = () => {
  //     const currentTheme = theme === 'system' ? systemTheme : theme
  //     if (currentTheme === 'dark') {
  //       return (
  //         <Button>
  //           <ModeIcon />
  //         </Button>
  //       )
  //     }
  //   }
  return (
    <>
      <div className="w-full h-24 flex items-center justify-center">
        <div className=" w-11/12  flex items-center justify-between">
          {/* Logo */}
          <div className="">
            <img src="./logolight.png" alt="logo" />
          </div>
          {/* Menu Items */}
          <div className="hidden md:flex space-x-10 ">
            {menuItems.map((menuItem, index) => {
              return (
                <div
                  key={index}
                  className="text-base text-base  hover:text-primary"
                >
                  <Link href={menuItem.link}>
                    <a>{menuItem.menu}</a>
                  </Link>
                </div>
              )
            })}
          </div>
          {/* Buttons */}
          <div className="flex  space-x-6">
            <button className=" hidden md:block bg-secondary text-primary font-base w-44 py-2 border-2 border-primary">
              Sign in
            </button>
            <button className="hidden xl:block bg-primary text-white font-base w-44 py-2 border-2 border-primary ">
              Register
            </button>
            <button>
              <ModeIcon />
            </button>
            {/* hamburger Menu */}
            <button
              onClick={() => {
                setDisplay((display: any) => !display)
              }}
              id="menu-btn"
              className="block ml-20 hamburger md:hidden focus:outline-none"
            >
              <span className="hamburger-top"></span>
              <span className="hamburger-middle"></span>
              <span className="hamburger-bottom"></span>
            </button>
          </div>
          {/* mobile menu */}
        </div>
        <div className={`${display ? 'hidden' : ''} md:hidden`}>
          <div className="absolute flex flex-col items-center self-end py-8 mt-10 space-y-6 font-bold bg-white sm:w-auto sm:self-center left-6 right-6 drop-shadow-md">
            {menuItems.map((menuItem, index) => {
              return (
                <div
                  key={index}
                  className="text-base text-base  hover:text-primary"
                >
                  <Link href={menuItem.link}>
                    <a>{menuItem.menu}</a>
                  </Link>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </>
  )
}

export default Navbar
