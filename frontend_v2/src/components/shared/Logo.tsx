"use client";

import Link from "next/link";
import Image from "next/image";

import { useTheme } from "next-themes";

import logoDark from "../../../public/logoDark.svg";
import logoLight from "../../../public/logoLight.svg";

export default function Logo({ shouldChange }: { shouldChange?: boolean }) {
  const { theme } = useTheme();

  return (
    <Link href="/">
      {shouldChange ? (
        <Image
          priority
          quality={100}
          src={
            theme == "system"
              ? logoLight
              : theme == "dark"
              ? logoLight
              : logoDark
          }
          alt="Web3Bridge Logo"
          className="h-14 w-40"
        />
      ) : (
        <Image
          priority
          quality={100}
          src={logoDark}
          alt="Web3Bridge Logo"
          className="h-14 w-40"
        />
      )}
    </Link>
  );
}
