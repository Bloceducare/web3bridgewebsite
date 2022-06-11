import LogoDark from "../../../assests/logo-dark.svg";
import Image from "next/image";
import {
  FacebookIcon,
  LinkedInIcon,
  TwitterIcon,
  YoutubeIcon,
  InstagramIcon,
} from "./icons";
import Link from "next/link";

const Footer = () => {
  return (
    <footer className="bg-[#000]  w-full px-10 py-5">
      <div className="w-full">
        <Image src={LogoDark} />
      </div>
      <div className="w-full flex items-start mt-4 text-white">
        <div className="w-[25%] mr-auto">
          <p className="text-white">Support@web3bridge.com</p>
          <div className="flex items-center w-[80%] justify-between">
            <TwitterIcon />
            <LinkedInIcon />
            <FacebookIcon />
            <InstagramIcon />
            <YoutubeIcon />
          </div>
        </div>
        <div className="w-[20%]">
          <h1 className="font-bold mb-4">Web 3 Bridge</h1>
          <ul className="text-xs ">
            <li className="my-1">
              <Link href={"/"}>
                <a>About us</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>Courses</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>Partners</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>Alumni</a>
              </Link>
            </li>
          </ul>
        </div>
        <div className="w-[20%]">
          <h1 className="font-bold mb-4">Support</h1>
          <ul className="text-xs ">
            <li className="my-1">
              <Link href={"/"}>
                <a>Terms of service</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>Privacy Policy</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>dApps</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>FAQ</a>
              </Link>
            </li>
          </ul>
        </div>
        <div className="w-[20%]">
          <h1 className="font-bold mb-4">General</h1>
          <ul className="text-xs ">
            <li className="my-1">
              <Link href={"/"}>
                <a>Join Community</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>Events</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>Resources</a>
              </Link>
            </li>
            <li className="my-1">
              <Link href={"/"}>
                <a>Links</a>
              </Link>
            </li>
          </ul>
        </div>
      </div>
      <p className="text-center text-white text-xs py-4 mt-10">
        All rights reserved 2022
      </p>
    </footer>
  );
};

export default Footer;
