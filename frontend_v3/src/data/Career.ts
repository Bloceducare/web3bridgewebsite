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
    id:"1",
    title: "Video Editor",
    tags: ["Full-time"],
    category: "Product",
    description:
      "We are seeking a talented and passionate Video Editor to join our dynamic media team. The ideal candidate will have a solid foundation in video editing techniques and a keen eye for storytelling. You will contribute to creating captivating content for our various platforms, ensuring our message reaches and resonates with our audience",
  },
  // {
  //   title: "Senior Product designer",
  //   tags: ["Hybrid", "Full-time"],
  //   category: "Design",
  //   description:
  //     "Since 2019 we've worked on 30+ major projects from 8 different industries that are being used by 500,000+ users and 1000+ businesses from 70+ different countries. Need full-cycle product development or an improvement cycle? Let's talk!",
  // },
  {
    id: "2",
    title: "secretary",
    tags: ["Full-time"],
    category: "Marketing",
    description:
      "We are seeking a highly organized and detail-oriented Secretary to join our dynamic team. The Secretary will play a critical role in managing key administrative tasks for our cohort programs and maintaining smooth communication within the team and with external stakeholders. The ideal candidate will be responsible for managing important documents, coordinating schedules, and ensuring the timely execution of tasks.",
  },

];

export const categories = [
  { name: "All Openings", count: allJobOpenings.length },
  { name: "Product", count: 3 },
  { name: "Design", count: 1 },
  { name: "Operation", count: 1 },
  { name: "Marketing", count: 2 },
];
