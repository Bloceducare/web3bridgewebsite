import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const navLinks = [
  {
    name: "Welcome",
    href: "/",
  },
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
    name: "Team",
    href: "/team",
  },
  {
    name: "Blog",
    href: "https://medium.com/@web3bridge",
    target: "_blank",
  },
  {
    name: "Events",
    href: "/events",
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
        path: "/trainings",
      },
      {
        name: "Partners",
        path: "/",
      },
      {
        name: "Alumni",
        path: "/cohorts",
      },
    ],
  },
  {
    title: "General",
    links: [
      {
        name: "Join Community",
        path: "https://t.me/web3bridge",
      },
      {
        name: "Events",
        path: "/events",
      },
      {
        name: "DApps",
        path: "/dapps",
      },
      {
        name: "Blog",
        path: "https://medium.com/@web3bridge",
      },
    ],
  },
  {
    title: "Support",
    links: [
      {
        name: "Terms of Use",
        path: "",
      },
      {
        name: "Privacy Policy",
        path: "",
      },
      {
        name: "Resources",
        path: "",
      },
      {
        name: "FAQ",
        path: "",
      },
    ],
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

export const TeamMembers = [
  {
    name: "Awosika Israel Ayodeji",
    role: "Founder, Program Manager",
    image: "/about/Oga.JPG",
  },

  {
    name: "Akinnusotu Temitayo",
    role: "Co-founder, Lead Dev/Mentor",
    image: "/about/Timidan.jpg",
  },
  {
    name: "Olusanya Oluwagbeminiyi",
    role: "Community Manager",
    image: "/about/Oluwa.jpeg",
  },

  {
    name: "Samuel Babalola",
    role: "Operations Lead",
    image: "/about/Sam.jpeg",
  },
  {
    name: "Ajayi O. Samuel",
    role: "Media Lead",
    image: "/about/aj.jpeg",
  },
  {
    name: "Dominion Majemu-Itura",
    role: "Media",
    image: "/about/nic.JPG",
  },
  {
    name: "John Deborah",
    role: "HR/Facility Manager",
    image: "/about/debi.JPEG",
  },
  {
    name: "Goodness Kolapo ",
    role: "Developer/PM",
    image: "/about/Team11.png",
  },
  {
    name: "Ayomide Arowolo",
    role: "Academic Operations and Curriculum Design Lead",
    image: "/about/ayo_img.jpeg",
  },
];

export const isValidEthereumAddress = (address: string) => {
  // Ethereum address regex pattern
  const pattern = /^(0x)?[0-9a-fA-F]{40}$/;
  return pattern.test(address);
};
