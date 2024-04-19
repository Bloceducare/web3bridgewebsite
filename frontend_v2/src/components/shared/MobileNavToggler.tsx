"use client";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { HamburgerMenuIcon } from "@radix-ui/react-icons";
import Logo from "./Logo";
import Link from "next/link";
import { cn, navLinks } from "@/lib/utils";
import { usePathname } from "next/navigation";
import {
    Sheet,
    SheetContent,
    SheetClose,
    SheetTrigger,
} from "@/components/ui/sheet";

export const MobileNavToggler = () => {
    const pathname = usePathname();

    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="outline" size="icon">
                    <HamburgerMenuIcon />
                </Button>
            </SheetTrigger>
            <SheetContent>
                <main className="w-full flex flex-col gap-16">
                    <div className="w-full flex justify-between items-center">
                        <Logo />
                    </div>
                    <ul className="flex flex-col gap-6 pl-2">
                        {navLinks.map((link) => (
                            <li key={link.name}>
                                <SheetClose asChild>
                                    <Link
                                        href={link.href}
                                        className={cn(
                                            "text-base font-normal text-muted-foreground  transition",
                                            {
                                                "text-bridgeRed": link.href == pathname,
                                                "hover:text-foreground": link.href != pathname,
                                            }
                                        )}>
                                        {link.name}
                                    </Link>
                                </SheetClose>
                            </li>
                        ))}
                    </ul>
                </main>
            </SheetContent>
        </Sheet>
    );
};
