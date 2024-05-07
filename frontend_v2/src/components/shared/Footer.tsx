"use client";

import MaxWrapper from "./MaxWrapper";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import Link from "next/link";
import { cn, footerLinks } from "@/lib/utils";
import { usePathname } from "next/navigation";
import logoLight from "../../../public/logo-light.svg";

import { FaSquareTwitter } from "react-icons/fa6";
import { FaLinkedin } from "react-icons/fa";
import { RiInstagramFill } from "react-icons/ri";
import { TbBrandYoutubeFilled } from "react-icons/tb";
import Image from "next/image";

export default function Footer() {
  const pathname = usePathname();

  return (
    <footer className="border-t border-[#6E6E6E]/50 text-black w-full py-10 bg-gradient-to-b from-red-100 via-red-200 to-background mt-20">
      <MaxWrapper className="flex gap-6 flex-col lg:flex-row">
        <div className="w-full lg:w-[451px] rounded-2xl bg-[#1B1B1B] p-6 flex flex-col gap-2">
          <h1 className="font-bold text-2xl w-full lg:w-[225px] text-[#FFFBF3]">
            Subscribe To Our Newsletter
          </h1>
          <p className="text-base text-[#FFFBF3] font-normal">
            Get occasional news and update from us about the latest trends,
            technology in the web 3 world, we promise not to spam you.
          </p>

          <form
            action="https://c75e802e.sibforms.com/serve/MUIFALe4lAOyLtL5vTm4hUf2XWF8FBC_TcuQ0kg1mauaBFLU8O8M5dnWtIJRiLGFZb3FDU-mU-H6Je0wsVrAV_5fBy6Xxt9j3xLoBuy_DWo7I2HJ7rNIDyBGPsBx_ZO_UDXheNqbd0vZKQiZCZBAwWNw0H0FwGt10qUK-VRlj807pjEZfs_uJqM8CK2gVfF9BL0pv9DohGVZYrwK"
            method="post"
            className="mt-auto ">
            <div className="mt-10 flex items-center flex-col md:flex-row gap-4">
              <Input
                placeholder="Email address"
                className="rounded-full h-12 px-4 text-white"
              />
              <Button className="h-12 w-full md:w-max rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-white hover:bg-transparent">
                Subscribe <MoveRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </form>
        </div>

        <div className="bg-white/70 backdrop-blur-md h-full flex-1 px-8 py-10 rounded-2xl">
          <div className="flex flex-wrap flex-col-reverse sm:flex-row justify-between gap-14">
            {footerLinks.map((route) => (
              <div className="flex flex-col" key={route.title}>
                <h1 className="text-base font-normal text-[#6E6E6E] capitalize">
                  {route.title}
                </h1>

                <div className="mt-6 flex flex-col gap-4">
                  {route.links.map((link, _key) => (
                    <Link
                      key={_key}
                      href={link.path}
                      className={cn("text-sm font-medium capitalize", {
                        "text-red-500": link.path == pathname,
                      })}>
                      {link.name}
                    </Link>
                  ))}
                </div>
              </div>
            ))}

            <Link href="/">
              <Image
                priority
                quality={100}
                src={logoLight}
                alt="Web3Bridge Logo"
                className="h-14 w-40"
              />
            </Link>
          </div>

          <div className="flex items-center justify-between gap-3 flex-wrap mt-10">
            <div className="flex items-center gap-4">
              <p className="text-sm text-muted-foreground">
                Support@web3bridge.com
              </p>

              <div className="flex items-center gap-2">
                <Link href="/">
                  <FaSquareTwitter className="w-5 h-5" />
                </Link>
                <Link href="/">
                  <FaLinkedin className="w-5 h-5" />
                </Link>
                <Link href="/">
                  <RiInstagramFill className="w-5 h-5" />
                </Link>
                <Link href="/">
                  <TbBrandYoutubeFilled className="w-5 h-5" />
                </Link>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2023 All Rights Reserved
            </p>
          </div>
        </div>
      </MaxWrapper>
    </footer>
  );
}
