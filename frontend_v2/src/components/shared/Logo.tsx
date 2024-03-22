"use client";
import Link from "next/link";
import Image from "next/image";

import { useTheme } from "next-themes";

import logoDark from "../../../public/logo-dark.svg";
import logoLight from "../../../public/logo-light.svg";

export default function Logo() {
  const { theme } = useTheme();

  return (
    <Link href="/">
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
    </Link>
  );
}
