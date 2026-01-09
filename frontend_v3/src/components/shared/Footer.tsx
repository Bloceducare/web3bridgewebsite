"use client";

import MaxWrapper from "./MaxWrapper";
import { Input } from "@/components/ui/input";
import { Button, buttonVariants } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import Link from "next/link";
import { cn, footerLinks } from "@/lib/utils";
import { usePathname } from "next/navigation";
import logoDark from "../../../public/logo-dark.svg";

import { FaSquareTwitter } from "react-icons/fa6";
import { FaLinkedin } from "react-icons/fa";
import { RiInstagramFill } from "react-icons/ri";
import { TbBrandYoutubeFilled } from "react-icons/tb";
import Image from "next/image";
import { footerIcons } from "@/data/footer_icons";

export default function Footer() {
  const pathname = usePathname();

  return (
    <footer className=" text-black w-full py-24 bg-[url('/footer_image.png')] bg-contain" >
      <MaxWrapper className="flex gap-6 flex-col items-center lg:flex-row">
        <div className="w-full lg:w-[451px] rounded-2xl p-[2px] bg-gradient-to-b from-[hsla(0,0%,14%,1)] to-[hsla(40,0%,28%,0.67)] backdrop-blur-sm ">
          <div className="w-full h-full bg-[hsl(330,3%,12%)]  rounded-2xl ">
            <div className="w-full h-full rounded-2xl shadow-[inset_1px_16px_32px_hsla(332,100%,89%,0.08)] bg-[hsla(330,3%,12%,0.31)] p-6 flex flex-col gap-2">
              <h1 className="font-bold text-[28px] w-full text-[#FFFBF3]">
                Subscribe To Our Newsletter
              </h1>
              <p className="text-base text-[#FFFBF3] font-normal">
                Stay up to date from with us about the latest  news, trends, technology in the web 3 world, we promise not to spam you.</p>

              <form
                action="https://c75e802e.sibforms.com/serve/MUIFALe4lAOyLtL5vTm4hUf2XWF8FBC_TcuQ0kg1mauaBFLU8O8M5dnWtIJRiLGFZb3FDU-mU-H6Je0wsVrAV_5fBy6Xxt9j3xLoBuy_DWo7I2HJ7rNIDyBGPsBx_ZO_UDXheNqbd0vZKQiZCZBAwWNw0H0FwGt10qUK-VRlj807pjEZfs_uJqM8CK2gVfF9BL0pv9DohGVZYrwK"
                method="post"
                className="mt-auto ">
                <div className="mt-10 flex items-center flex-col space-y-6">
                  <Input
                    placeholder="Email address"
                    className="rounded-lg h-14 px-4 text-white"
                  />
                  <Button className={cn(buttonVariants({ variant: "bridgePrimary" }), "h-12 w-full rounded-full hover:bg-bridgeRed/80")}>
                    Subscribe <MoveRight className="w-5 h-5 ml-2" />
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div className=" backdrop-blur-md h-full flex-1 px-8 py-10 rounded-2xl">
          <div className="flex flex-wrap flex-col-reverse sm:flex-row justify-between gap-14">
            {footerLinks.map((route) => (
              <div className="flex flex-col" key={route.title}>
                <h1 className="text-base font-normal text-white capitalize">
                  {route.title}
                </h1>

                <div className="mt-6 flex flex-col gap-4">
                  {route.links.map((link, _key) => (
                    <Link
                      key={_key}
                      href={link.path}
                      className={cn("text-sm text-white font-medium capitalize")}>
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
                src={logoDark}
                alt="Web3Bridge Logo"
                className="h-14 w-40"
              />
            </Link>
          </div>

          <div className="flex flex-col space-y-10 gap-3 flex-wrap mt-10">
            <div className="flex items-center gap-4">
              <p className="text-lg text-muted-foreground">
                support@web3bridge.com &#9679;
              </p>

              <div className="flex items-center gap-2">
                {
                  footerIcons.map(({ id, description, imageUrl, href }) =>
                    <Link href={href} key={id} className="w-12 h-12 relative">
                      <Image src={imageUrl} fill className="object-contain" alt={description} />
                    </Link>

                  )
                }
              </div>
            </div>
            <p className="text-lg text-muted-foreground">
              © 2023 All Rights Reserved
            </p>
          </div>
        </div>
      </MaxWrapper>
    </footer >
  );
}
