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
    image: "/about/Team1.png"
  },

  {
    name: "Akinnusotu Temitayo",
    role: "Co-founder, Lead Dev/Mentor",
    image: "/about/Team2.png"
  },
  {
    name: "Katangole Allan",
    role: "Head, Technical Training",
    image: "/about/Team3.png"
  },
  {
    name: "Jeremiah Noah",
    role: "Lead dev/ Mentor",
    image: "/about/Team4.png"
  },

  {
    name: "Oke Kehinde",
    role: "Blockchain Developer/ Mentor",
    image: "/about/Team5.png"
  },
  {
    name: "Abimbola Adebayo",
    role: "Blockchain Developer/ Mentor",
    image: "/about/Team6.png"
  },
  {
    name: "Falilat Owolabi",
    role: "Blockchain Developer/ Mentor",
    image: "/about/Team7.png"
  },
  {
    name: "Ademola Kelvin",
    role: "Blockchain Developer/ Mentor",
    image: "/about/Team8.png"
  },
  {
    name: "Yetunde Ige",
    role: "Project Manager",
    image: "/about/Team9.png"
  },
  {
    name: "Michael Jerry",
    role: "Community/ Social Media Lead",
    image: "/about/Team10.png"
  },
  {
    name: "Billy Luedtke",
    role: "Advisor & Angel investor",
    image: "/about/Team11.png"
  },
  {
    name: "Marek Laskowski, PhD",
    role: "Advisor, Founder Blockchain.lab",
    image: "/about/Team12.png"
  }
  ];