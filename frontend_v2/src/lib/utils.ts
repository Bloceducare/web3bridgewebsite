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

export const utilityIndex = [
  {
    percent: "100%",
    text: "Access to Web3bridge internal news discord channel (development and product update)",
  },
  {
    percent: "5%",
    text: "Access to token/equity share of all Web3bridge products/projects",
  },
  {
    percent: "10%",
    text: "Annual Income Sharing Agreement shares",
  },
  {
    percent: "25%",
    text: "Annual return on all development contract fund taken by Web3bridge dev team",
  },
];
