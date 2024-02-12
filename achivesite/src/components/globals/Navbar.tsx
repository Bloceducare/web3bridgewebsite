import { useState, useContext, useEffect, useMemo, useCallback } from "react";
import { ThemeContext } from "../ThemeContext";
import Link from "next/link";
import Image from "next/image";
import DarkLogo from "../../../assets/logo-dark.png";
import LightLogo from "../../../assets/logo-light.svg";
import { DarkModeIcon, LightModeIcon } from "./icons";
import { blurUrl, menuItems } from "data";
import { FaTimes } from "react-icons/fa";
import { GiHamburgerMenu } from "react-icons/gi";
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
        <div className="flex items-center justify-between w-11/12 z-55 md:w-full md:p-4 lg:w-11/12 lg:p-0">
          <div className="w-[140px]">
            {/* Logo */}
            <Link href="/">
              <a>
                {isLight ? (
                  <Image
                    src={LightLogo}
                    className=""
                    placeholder="blur"
                    blurDataURL={blurUrl}
                  />
                ) : (
                  <Image
                    src={DarkLogo}
                    placeholder="blur"
                    blurDataURL={blurUrl}
                  />
                )}
              </a>
            </Link>
          </div>

          {/* Menu Items */}
          <div className="hidden md:space-x-7 lg:space-x-10 md:flex ">
            {menuItems.map((menuItem, index) => {
              return (
                <div key={index} className="text-base hover:text-primary">
                  {menuItem.externalLink ? (
                    <a
                      href={menuItem.link}
                      target="_blank"
                      rel="noreferrer noopener"
                      className={`dark:text-white ${
                        router.pathname == menuItem.link
                          ? "text-primary dark:text-primary"
                          : ""
                      }`}
                    >
                      {menuItem.menu}
                    </a>
                  ) : (
                    <Link href={menuItem.link}>
                      <a
                        className={`dark:text-white ${
                          router.pathname == menuItem.link
                            ? "text-primary dark:text-primary"
                            : ""
                        }`}
                      >
                        {menuItem.menu}
                      </a>
                    </Link>
                  )}
                </div>
              );
            })}
          </div>
          {/* Buttons */}
          <div className="flex space-x-6">
            {/* <Link href="/cohort-registration">
              <a className="hidden md:block px-1 py-0 xl:block rounded-sm bg-primary text-white font-base md:px-2 lg:px-[1rem] xl:px-[2rem] md:py-1 border-2 border-primary ">
                Register for cohort VIII
              </a>
            </Link> */}
            {/* <button className="hidden md:block px-1 py-0 xl:block rounded-sm bg-primary text-white font-base md:px-2 lg:px-[1rem] xl:px-[2rem] md:py-1 border-2 border-primary ">

                <a
                  href="https://forms.gle/pc8d31R99fFp4Dzu5"
                  className="capitalize"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Join wait list 
                </a>
              </button> */}

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
              className="block mb-3 hamburger md:hidden focus:outline-none "
            >
              <GiHamburgerMenu className="dark:text-white" size={30} />
            </button>
          </div>
        </div>
        {/* mobile menu */}
        <div
          className={` ${
            display ? "w-0 scale-x-0" : "w-full z-10"
          } absolute left-0 top-0  md:hidden flex flex-col items-center self-end  space-y-6 font-bold bg-white dark:bg-base sm:self-center drop-shadow-md ease-in-out duration-300 `}
        >
          <div className="flex justify-between w-full px-5 py-3 shadow-md">
            <div
              className="w-[140px]"
              onClick={() => {
                setDisplay((display: any) => !display);
              }}
            >
              <Link href="/">
                <a>
                  {isLight ? (
                    <Image src={LightLogo} className="w-[140px]" />
                  ) : (
                    <Image src={DarkLogo} />
                  )}
                </a>
              </Link>
            </div>
            <button
              onClick={() => {
                setDisplay((display: any) => !display);
              }}
              className=" focus:outline-none"
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
                className="items-start w-full py-3 pl-10 text-base dark:text-white hover:text-primary"
              >
                <Link href={menuItem.link}>
                  <a
                    className={`dark:text-white ${
                      router.pathname == menuItem.link
                        ? "text-primary dark:text-primary"
                        : ""
                    }`}
                  >
                    {menuItem.menu}
                  </a>
                </Link>
              </div>
            );
          })}
          <div className="flex justify-between w-full px-10">
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
          <div className="flex flex-col w-full gap-6 px-10 py-14">
            <button className="rounde-sm lg:block bg-secondary text-primary font-base dark:text-white10 dark:bg-primary  lg:px-[1rem] xl:px-[2rem] py-2 border-2 border-primary">
              <a
                href="http://nft.web3bridge.com/"
                className="capitalize"
                target="_blank"
                rel="noopener noreferrer"
              >
                Web3bridge Nft
              </a>
            </button>

            {/* <button className="rounde-sm lg:block bg-secondary text-primary font-base dark:text-white10 dark:bg-primary  lg:px-[1rem] xl:px-[2rem] py-2 border-2 border-primary">
              <a
                href="/cohort-registration"
                className="capitalize"
                target="_blank"
                rel="noopener noreferrer"
              >
                Register for Cohort VIII
              </a>
            </button> */}
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
