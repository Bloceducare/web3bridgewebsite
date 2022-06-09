import { useContext } from "react";
import { ThemeContext } from "../components/ThemeContext";
import Image from "next/image";
import LogoLight from "../assests/about-us/logo-light.svg";
import DarkLight from "../assests/about-us/logo-dark.svg";
import Button from "./Button";
import Link from "next/link";
import Dark from "../assests/about-us/dark-mode-icon.svg";
import Light from "../assests/about-us/light-mode-icon.svg";
import NavAdvert from "../components/NavAdvert";

const Nav = () => {
  const { theme, setTheme } = useContext(ThemeContext);
  return (
    <>
      <NavAdvert />
      <nav className="w-full bg-white dark:bg-[#000] flex items-center px-8 py-4 border-b">
        {theme === "dark" ? (
          <Image src={DarkLight} />
        ) : (
          <Image src={LogoLight} className=" " />
        )}
        <ul className="flex ml-auto text-[#111111] dark:text-[white]">
          <li className="mx-4">
            <Link href={"/"}>
              <a>Home</a>
            </Link>
          </li>
          <li className="mx-4">
            <Link href={"/about-us"}>
              <a>About us</a>
            </Link>
          </li>
          <li className="mx-4">
            <Link href={"/"}>
              <a>Cohorts</a>
            </Link>
          </li>
          <li className="mx-4">
            <Link href={"/"}>
              <a>dApps</a>
            </Link>
          </li>
          <li className="mx-4">
            <Link href={"/alumni"}>
              <a>Alumni</a>
            </Link>
          </li>
          <li className="mx-4">
            <Link href={"/"}>
              <a>Hire us</a>
            </Link>
          </li>
        </ul>
        <div className="ml-auto mr-2 flex items-center">
          <Button class="mx-2 border-[#FA0101] text-[#FA0101] px-6 py-1" type="transparent" content="Sign in" />
          <Button class="mx-2  px-6 py-1" type="background" content="Register" />
        </div>

        {theme === "light" ? (
          <Image
            src={Dark}
            width={20}
            height={20}
            className=" cursor-pointer"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          />
        ) : (
          <Image
            src={Light}
            width={20}
            height={20}
            className=" cursor-pointer"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          />
        )}
      </nav>
    </>
  );
};

export default Nav;
