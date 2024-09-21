import clock from "../../public/career/Clock.svg";
import Barbell from "../../public/career/Barbell.svg";
import Confetti from "../../public/career/Confetti.svg";
import RocketLaunch from "../../public/career/RocketLaunch.svg";
export const benefitsData = [
  {
    icon: clock,
    title: "Work Hours Flexibility",
    bgColor:
      "bg-gradient-to-t from-transparent via-teal-100/20 to-teal-100/70 border-teal-500/40",
  },
  {
    icon: Barbell,
    title: "Health & Wellness",
    bgColor:
      "bg-gradient-to-t from-transparent via-amber-100/20 to-amber-100/70 border-amber-500/40",
  },
  {
    icon: Confetti,
    title: "Fun Team Events",
    bgColor:
      "bg-gradient-to-t from-transparent via-violet-200/20 to-violet-200/70 border-violet-500/40",
  },
  {
    icon: RocketLaunch,
    title: "Career Growth Opportunities",
    bgColor:
      "bg-gradient-to-t from-transparent via-rose-200/20 to-rose-200/70 border-rose-500/40",
  },
];

export const allJobOpenings = [
  {
    title: "Full-Stack Developers",
    tags: ["Full-time"],
    category: "Product",
    description:
      "Due to growing workload, we are looking for experienced and talented Full-Stack Developers to join our fast-paced Engineering team. You will work closely with Product, Design and Marketing to analyze, develop, debug, test, roll-out and support new and existing product features.",
  },
  {
    title: "Senior Product designer",
    tags: ["Hybrid", "Full-time"],
    category: "Design",
    description:
      "Since 2019 we've worked on 30+ major projects from 8 different industries that are being used by 500,000+ users and 1000+ businesses from 70+ different countries. Need full-cycle product development or an improvement cycle? Let's talk!",
  },
  {
    title: "Media/Creative Director",
    tags: ["Full-time"],
    category: "Marketing",
    description:
      "We've worked on 30+ major projects from 8 different industries that are being . Need full-cycle product development or an improvement cycle? Let's talk!",
  },
  {
    title: "Software Development Intern",
    tags: ["Internship"],
    category: "Product",
    description:
      "Join our Engineering team as a Software Development Intern. You'll gain hands-on experience working on real projects, collaborating with experienced developers, and learning industry-standard practices in software development.",
  },
  {
    title: "UX/UI Design Intern",
    tags: ["Internship"],
    category: "Design",
    description:
      "We're seeking creative and enthusiastic UX/UI Design Interns to assist our design team. You'll be involved in user research, wireframing, prototyping, and contributing to the design of our digital products.",
  },
  {
    title: "Marketing Assistant",
    tags: ["Part-time"],
    category: "Marketing",
    description:
      "We're looking for students passionate about marketing to join our team part-time. You'll assist in creating content, managing social media, and learning about digital marketing strategies in a fast-paced environment.",
  },
  {
    title: "Operations Manager",
    tags: ["Full-time"],
    category: "Operation",
    description:
      "We're seeking an experienced Operations Manager to oversee and optimize our business processes. You'll work across departments to ensure efficient operations and drive continuous improvement.",
  },
];

export const categories = [
  { name: "All Openings", count: allJobOpenings.length },
  { name: "Product", count: 3 },
  { name: "Design", count: 1 },
  { name: "Operation", count: 4 },
  { name: "Marketing", count: 2 },
];
