"use client";
import Link from "next/link";
import Image from "next/image";
import { useTheme } from "next-themes";
import logoDark from "../../../public/logo-dark.svg";
import logoLight from "../../../public/logo-light.svg";
import { useEffect, useState } from "react";

export default function Logo() {
  const { resolvedTheme, systemTheme } = useTheme();

  const [currentTheme, setCurrentTheme] = useState(
    resolvedTheme === "system" ? systemTheme : resolvedTheme
  );

  useEffect(() => {
    setCurrentTheme(resolvedTheme === "system" ? systemTheme : resolvedTheme);
  }, [resolvedTheme, systemTheme]);

  return (
    <Link href="/">
      <Image
        priority
        quality={100}
        src={currentTheme === "dark" ? logoDark : logoLight}
        alt="Web3Bridge Logo"
        className="h-14 w-40"
      />
    </Link>
  );
}
