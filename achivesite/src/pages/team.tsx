import React, { Fragment } from "react";
import HeaderImg from "../../assets/about-us/about-header-image.svg";
import GroupImg from "../../assets/about-us/group-image.svg";
import Founder from "../../assets/about-us/founder.png";
import Cofounder from "../../assets/about-us/Cofounder.svg";
import Head from "../../assets/about-us/Head.svg";
import LeadDev from "../../assets/about-us/LeadDev.svg";
import Oke from "../../assets/about-us/oke.png";
import Pelumi from "../../assets/about-us/Pelumi.png";
import Abims from "../../assets/about-us/Abims.png";
import Falilat from "../../assets/about-us/Falilat.png";
import Kevin from "../../assets/about-us/Kevin.png";
import Jerry from "../../assets/about-us/jerry.png";
import Billy from "../../assets/about-us/billy.png";
import Yetunde from "../../assets/about-us/Yetunde.png";
import Ezra from "../../assets/about-us/Ezra.png";
import Marek from "../../assets/about-us/marek.png";
import Image from "next/image";
import Button from "../components/Button";
import type { NextPage } from "next";
type Images = {
  name: string;
  role: string;
  image: any;
};
const About: NextPage = () => {
  const images: Images[] = [
    {
      name: "Awosika Israel Ayodeji",
      role: "Founder, Program Manager",
      image: Founder,
    },
    {
      name: "Akinnusotu Temitayo Daniel",
      role: "Co-founder, Lead Dev/Mentor",
      image: Cofounder,
    },
    {
      name: "Katangole Allan",
      role: "Head, Technical Training",
      image: Head,
    },
    {
      name: "Jeremiah Noah",
      role: "Lead dev/ Mentor",
      image: LeadDev,
    },
    {
      name: "Oke Kehinde",
      role: "Blockchain Developer/ Mentor",
      image: Oke,
    },
    {
      name: "Fatolu Pelumi",
      role: "Blockchain Developer/ Mentor",
      image: Pelumi,
    },
    {
      name: "Abimbola Adebayo",
      role: "Blockchain Developer/ Mentor",
      image: Abims,
    },
    {
      name: "Falilat Owolabi",
      role: "Blockchain Developer/ Mentor",
      image: Falilat,
    },
    {
      name: "Ademola Kelvin",
      role: "Blockchain Developer/ Mentor",
      image: Kevin,
    },
    {
      name: "Michael Jerry",
      role: "Community/ Social Media Lead",
      image: Jerry,
    },
    {
      name: "Suleman U. Ezra",
      role: "Lead Designer",
      image: Ezra,
    },
    {
      name: "Yetunde Ige",
      role: "Project Manager",
      image: Yetunde,
    },
    {
      name: "Marek Laskowski, PhD",
      role: "Advisor, Founder Blockchain.lab (York University). Founder Blockchain Hub. Vice Chair, UN/CEFACT (Methodology & Technology)",
      image: Marek,
    },
    {
      name: "Billy Luedtke",
      role: "Advisor & Angel investor",
      image: Billy,
    },
  ];
  return (
    <Fragment>
      <section className="mt-[2rem] px-12 md:mt-[5rem]">
        <h1 className="dark:text-[#D0D0D0] text-center mb-19 font-bold text-2xl md:text-[3rem] my-12 md:mb-24">
          Meet The Team
        </h1>
        <div className=" flex flex-wrap w-full justify-around md:justify-start">
          {images.map((items, index) => {
            return (
              <div
                key={index}
                className=" w-[90%] sm:w-[45%] md:w-[30%] text-center mb-11 sm:mb-24  md:mr-[1.5rem] text-white">
                <Image
                  key={index}
                  src={items?.image}
                  height={400}
                  width={400}
                />
                <h1 className="text-xl text-[#151515] dark:text-white font-bold">
                  {items?.name}
                </h1>
                <p className="text-[#A1A1A1] w-full">{items?.role}</p>
              </div>
            );
          })}
        </div>
      </section>
    </Fragment>
  );
};

export default About;
