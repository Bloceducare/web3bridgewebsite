import { useContext } from "react";
import { ThemeContext } from "../components/ThemeContext";
import Image from "next/image";
import LogoLight from "../assests/logo-light.svg";
import DarkLight from "../assests/logo-dark.svg";
import Button from "./Button";
import Link from "next/link";
import Dark from "../assests/dark-mode-icon.svg";
import Light from "../assests/light-mode-icon.svg";
type Props = {};

const Nav = (props: Props) => {
  const { theme, setTheme } = useContext(ThemeContext);
  return (
    <nav className="w-full bg-white dark:bg-[#111111] flex items-center px-8 py-4 border-b">
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
          <Link href={"/"}>
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
          <Link href={"/"}>
            <a>Alumni</a>
          </Link>
        </li>
        <li className="mx-4">
          <Link href={"/"}>
            <a>Hire us</a>
          </Link>
        </li>
      </ul>
      <div className="ml-auto flex items-center">
        <Button class="mx-2 px-6 py-1" type="transparent" content="Sign in" />
        <Button class="mx-2 px-6 py-1" type="background" content="Register" />
        {theme === "light" ? (
          <Image
            src={Dark}
            className="ml-6 cursor-pointer"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          />
        ) : (
          <Image
            src={Light}
            className="ml-6 cursor-pointer"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          />
        )}
      </div>
    </nav>
  );
};

export default Nav;
