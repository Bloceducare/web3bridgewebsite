import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const navLinks = [
  {
    name: "Home",
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
    name: "Blog",
    href: "https://medium.com/@web3bridge",
    target: "_blank",
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
    name: "Career",
    href: "/career",
  },
];

export const footerLinks = [
  {
    title: "Web3Bridge",
    links: [
      {
        name: "About Us",
        path: "",
      },
      {
        name: "Courses",
        path: "",
      },
      {
        name: "Partners",
        path: "",
      },
      {
        name: "Alumni",
        path: "",
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
        path: "",
      },
      {
        name: "Privacy Policy",
        path: "",
      },
      {
        name: "FAQ",
        path: "",
      },
    ],
  },
  {
    title: "general",
    links: [
      {
        name: "Join Community",
        path: "",
      },
      {
        name: "Events",
        path: "",
      },
      {
        name: "Resources",
        path: "",
      },
      {
        name: "Blog",
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
    role: "Community manager",
    image: "/about/Oluwa.jpeg",
  },

  {
    name: "Ekoh Victor",
    role: "Marketing Lead",
    image: "/about/Victor.jpg",
  },
  //Victor.jpg

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
    name: "Oluwadunsin Marcus",
    role: "Social Media",
    image: "/about/Marc.jpeg",
  },
  {
    name: "Monte Christian",
    role: "Designer",
    image: "/about/Christian.jpg",
  },
  {
    name: "Goodness Kolapo ",
    role: "Developer/PM",
    image: "/about/Team11.png",
  },
  // {
  //   name: "Goodness Kolapo ",
  //   role: "Developer/PM",
  //   image: "/about/Team8.png",
  // },
];

export const isValidEthereumAddress = (address: string) => {
  // Ethereum address regex pattern
  const pattern = /^(0x)?[0-9a-fA-F]{40}$/;
  return pattern.test(address);
};
