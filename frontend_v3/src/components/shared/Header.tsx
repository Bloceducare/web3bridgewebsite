"use client";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { ModeToggle } from "@/components/shared/ModeToggle";
import Logo from "./Logo";
import Link from "next/link";
import { cn, navLinks } from "@/lib/utils";
import { usePathname } from "next/navigation";
import { MobileNavToggler } from "./MobileNavToggler";
import { useScroll, motion, useSpring } from "framer-motion";
import { buttonVariants } from "../ui/button";

export default function Header() {
  const pathname = usePathname();
  const { scrollYProgress } = useScroll();

  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001,
  });

  return (
    <>
      <motion.div
        className=" fixed top-0 left-0 right-0 bg-bridgeRed origin-[0%] h-[5px] z-[42]"
        style={{ scaleX }}
      />
      <div className=" fixed top-0 inset-x-0 z-40 w-full py-3 lg:pt-5 dark:backdrop-blur-3xl">
        <MaxWrapper className="h-full w-full flex items-center justify-between gap-10">
          <Logo />

          <div className="h-20 border rounded-full hidden bg-[#FB8888]/5 lg:flex items-center justify-center gap-6 px-6">
            {navLinks.map((link, _key) => (
              <Link
                href={link.href}
                target={link.target}
                key={_key}
                className={cn(
                  "text-base font-normal text-muted-foreground  transition",
                  {
                    "text-bridgeRed": link.href == pathname,
                    "hover:text-foreground": link.href != pathname,
                  },
                )}
              >
                {link.name}
              </Link>
            ))}
            <Link
              href="/register"
              className={buttonVariants({
                variant: "secondary"
              })}
            >
              Join Next Cohort
            </Link>
            <Link
              href="/partner"
              
              className={buttonVariants({
                variant:"bridgeOutline"
              })}
            >
              Partner With Us
            </Link>
          </div>

          <div className="flex items-center justify-end gap-3 flex-1 max-w-[160px]">
            <ModeToggle />

            <div className="lg:hidden">
              <MobileNavToggler />
            </div>
          </div>
        </MaxWrapper>
      </div>
    </>
  );
}
