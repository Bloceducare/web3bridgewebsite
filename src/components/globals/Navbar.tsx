import React, { useState, useContext, useEffect } from "react";
import { ThemeContext } from "../ThemeContext";
import Link from "next/link";
import Image from "next/image";
import DarkLogo from "../../../assests/logo-dark.svg";
import LightLogo from "../../../assests/logo-light.svg";
import { DarkModeIcon, LightModeIcon } from "./icons";
import { menuItems } from "../../Data";
import { FaTimes } from "react-icons/fa";
import { GiHamburgerMenu } from "react-icons/gi";
import { motion } from "framer-motion";
import { useRouter } from "next/router";

const Navbar = () => {
  const [display, setDisplay] = useState<any>(true);
  const [isLight, setIsLight] = useState<boolean>(false);
  const { theme, setTheme } = useContext(ThemeContext);
  const router = useRouter();

  useEffect(() => {
    if (theme === "light") {
      setIsLight(true);
    } else {
      setIsLight(false);
    }
  }, [theme]);
  return (
    <>
      <nav className="relative w-full border-b border-[#D0D0D0] dark:border-0 h-24 flex flex-col items-center justify-center dark:bg-base">
        <div className="z-55  w-11/12  flex items-center justify-between md:w-full md:p-4 lg:w-11/12 lg:p-0">
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
              );
            })}
          </div>
          {/* Buttons */}
          <div className="flex  space-x-6">
            {/* <motion.button
              whileTap={{ scale: 0.1 }}
              transition={{ duration: 0.6 }}
              className=" hidden lg:block bg-secondary text-primary font-base  lg:px-[1rem] xl:px-[2rem] py-1 border-2 border-primary"
            >
              Sign in
            </motion.button> */}
            <motion.button
              whileTap={{ scale: 0.1 }}
              transition={{ duration: 0.6 }}
              className=" hidden md:block px-1 py-0 xl:block rounded-sm bg-primary text-white font-base md:px-2 lg:px-[1rem] xl:px-[2rem] md:py-1 border-2 border-primary "
            >
              <button className="rounde-lg">
                <a
                  href="https://forms.gle/pc8d31R99fFp4Dzu5"
                  className="capitalize"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Join wait list
                </a>
              </button>
            </motion.button>
            {isLight ? (
              <button
                className="hidden md:block"
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              >
                <DarkModeIcon />
              </button>
            ) : (
              <button
                className="hidden md:block"
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              >
                <LightModeIcon />
              </button>
            )}

            {/* hamburger Menu */}

            <button
              onClick={() => {
                setDisplay((display: any) => !display);
              }}
              id="menu-btn"
              className="block mb-3 hamburger md:hidden focus:outline-none  "
            >
              <GiHamburgerMenu className="dark:text-white" size={30} />
            </button>
          </div>
        </div>
        {/* mobile menu */}
        <div
          className={` ${
            display ? "w-0 scale-x-0" : "w-full z-10"
          } absolute left-0 top-0  h-[100vh] md:hidden flex flex-col items-center self-end  space-y-6 font-bold bg-white dark:bg-base sm:self-center drop-shadow-md ease-in-out duration-300 `}
        >
          <div className="w-full flex justify-between px-5 py-3 shadow-md">
            {isLight ? (
              <Image src={LightLogo} className="" />
            ) : (
              <Image src={DarkLogo} />
            )}
            <button
              onClick={() => {
                setDisplay((display: any) => !display);
              }}
              className=" focus:outline-none "
            >
              <FaTimes size={20} color="#FA0101" />
            </button>
          </div>

          {menuItems.map((menuItem, index) => {
            return (
              <div
                onClick={() => {
                  setDisplay((display: any) => !display);
                }}
                key={index}
                className="w-full pl-10 py-3 text-base dark:text-white hover:text-primary items-start"
              >
                <Link href={menuItem.link}>
                  <a>{menuItem.menu}</a>
                </Link>
              </div>
            );
          })}
          <div className="w-full px-10 flex justify-between">
            <p className="text-base dark:text-white hover:text-primary">
              Theme
            </p>
            <div className="">
              {isLight ? (
                <button
                  className=""
                  onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                >
                  <DarkModeIcon />
                </button>
              ) : (
                <button
                  onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                >
                  <LightModeIcon />
                </button>
              )}
            </div>
          </div>
          <div className="w-full py-14 px-10 gap-6 flex flex-col">
            <button className="rounde-sm lg:block bg-secondary text-primary font-base  lg:px-[1rem] xl:px-[2rem] py-2 border-2 border-primary">
              <a
                href="https://forms.gle/pc8d31R99fFp4Dzu5"
                className="capitalize"
                target="_blank"
                rel="noopener noreferrer"
              >
                Join wait list
              </a>
            </button>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
