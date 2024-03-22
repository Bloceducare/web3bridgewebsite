'use client';
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
        src={
          theme === "dark"
            ? logoDark
            : theme === "system"
              ? logoDark
              : logoLight
        }
        alt="Web3Bridge Logo"
        className="h-12 w-36 lg:h-14 lg:w-40"
      />
    </Link>
  );
}
