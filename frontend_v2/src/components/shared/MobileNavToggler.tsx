'use client'
import React, { useState } from 'react'
import { Button } from "@/components/ui/button";
import { HamburgerMenuIcon, Cross1Icon } from "@radix-ui/react-icons";
import Logo from "./Logo";
import Link from "next/link";
import { cn, navLinks } from '@/lib/utils';
import { usePathname } from 'next/navigation';

export const MobileNavToggler = () => {

    const pathname = usePathname();

    const [open, setOpen] = useState(false);

    const handleToggle = () => {
        setOpen(!open);
    };
    return (
        <>
            <Button variant="outline" size="icon" onClick={handleToggle}>
                <HamburgerMenuIcon />
            </Button>
            {/* Mobile Nav  */}
            <nav
                className={`flex justify-end lg:hidden h-screen w-full dark:bg-red-700 bg-black/90 fixed top-0  ${open ? "right-0" : "-right-[120vw]"
                    } z-[9999] transition-all duration-500 ease-out`}
            >
                <div
                    className={`w-[70%] h-screen bg-background flex flex-col justify-between items-center relative ${open ? "right-0" : "-right-[120vw]"
                        } transition-all duration-500 ease-out delay-300`}
                >
                    <section className="w-full px-4 py-6 flex flex-col h-full justify-between gap-16">
                        <main className="w-full flex flex-col gap-16">
                            <div className="w-full flex justify-between items-center">
                                <Logo />
                                <Button variant="outline" size="icon" onClick={handleToggle}>
                                    <Cross1Icon />
                                </Button>
                            </div>
                            <ul className="flex flex-col gap-6 pl-2">
                                {navLinks.map((link) => (
                                    <li key={link.name}>
                                        <Link
                                            href={link.href}
                                            className={cn(
                                                "text-base font-normal text-muted-foreground  transition",
                                                {
                                                    "text-bridgeRed": link.href == pathname,
                                                    "hover:text-foreground": link.href != pathname,
                                                }
                                            )}
                                            onClick={handleToggle}
                                        >
                                            {link.name}
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </main>
                    </section>
                </div>
            </nav>
        </>
    )
}