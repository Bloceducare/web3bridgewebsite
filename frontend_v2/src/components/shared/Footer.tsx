"use client";

import MaxWrapper from "./MaxWrapper";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import Link from "next/link";
import Logo from "./Logo";
import { cn, footerLinks } from "@/lib/utils";
import { usePathname } from "next/navigation";

import { FaSquareTwitter } from "react-icons/fa6";
import { FaLinkedin } from "react-icons/fa";
import { RiInstagramFill } from "react-icons/ri";
import { TbBrandYoutubeFilled } from "react-icons/tb";

export default function Footer() {
  const pathname = usePathname();

  return (
    <footer className="border-t border-[#6E6E6E] text-black w-full py-10 bg-gradient-to-b from-red-100 via-red-200 to-background mt-44">
      <MaxWrapper className="flex gap-6 flex-col lg:flex-row">
        <div className="w-full lg:w-[451px] rounded-2xl bg-[#1B1B1B] p-6 flex flex-col gap-2">
          <h1 className="font-bold text-2xl w-full lg:w-[225px] text-[#FFFBF3]">
            Subscribe To Our Newsletter
          </h1>
          <p className="text-base text-[#FFFBF3] font-normal">
            Get occasional news and update from us about the latest trends,
            technology in the web 3 world, we promise not to spam you.
          </p>

          <div className="mt-auto ">
            <div className="mt-10 flex items-center gap-4">
              <Input
                placeholder="Email address"
                className="rounded-full h-12 px-4 text-white"
              />
              <Button className="h-12 rounded-full border-2 ring-2 ring-red-500 border-red-300 bg-transparent text-white hover:bg-transparent">
                Subscribe <MoveRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </div>
        </div>

        <div className="bg-white/70 backdrop-blur-md h-full flex-1 px-8 py-10 rounded-2xl">
          <div className="flex flex-wrap flex-col-reverse sm:flex-row justify-between gap-14">
            {footerLinks.map((route) => (
              <div className="flex flex-col" key={route.title}>
                <h1 className="text-base font-normal text-[#6E6E6E] capitalize">
                  {route.title}
                </h1>

                <div className="mt-6 flex flex-col gap-4">
                  {route.links.map((link) => (
                    <Link
                      key={link.path}
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

            <Logo />
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
