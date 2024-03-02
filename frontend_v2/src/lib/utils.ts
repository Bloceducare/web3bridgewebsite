import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const navLinks = [
  {
    name: "Trainings",
    href: "/trainings",
  },
  {
    name: "Cohorts",
    href: "/cohorts",
  },
  {
    name: "About Us",
    href: "/about",
  },
  {
    name: "Blog",
    href: "/blog",
  },
  {
    name: "dApps",
    href: "/dapps",
  },
  {
    name: "NFTs",
    href: "/nfts",
  },
  {
    name: "Events",
    href: "/events",
  },
  {
    name: "Hire Us",
    href: "/hire",
  },
];

export const footerLinks = [
  {
    title: "Web3Bridge",
    links: [
      {
        name: "About Us",
        path: "/about",
      },
      {
        name: "Courses",
        path: "/courses",
      },
      {
        name: "Partners",
        path: "/partners",
      },
      {
        name: "Alumni",
        path: "/alumni",
      },
    ],
  },
  {
    title: "Supports",
    links: [
      {
        name: "DApps",
        path: "/dapps",
      },
      {
        name: "Terms of Use",
        path: "/terms-of-use",
      },
      {
        name: "Privacy Policy",
        path: "/privacy-policy",
      },
      {
        name: "FAQ",
        path: "/faq",
      },
    ],
  },
  {
    title: "general",
    links: [
      {
        name: "Join Community",
        path: "/community",
      },
      {
        name: "Events",
        path: "/events",
      },
      {
        name: "Resources",
        path: "/resources",
      },
      {
        name: "Blog",
        path: "/blog",
      },
    ],
  },
];
