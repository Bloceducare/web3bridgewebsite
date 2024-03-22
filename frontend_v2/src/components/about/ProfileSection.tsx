import React from "react";
import Image from "next/image";

import ProfileImg1 from "../../../public/about/ProfileImage1.png";
import ProfileImg2 from "../../../public/about/ProfileImage2.png";
import ProfileImg3 from "../../../public/about/ProfileImage3.png";
import ProfileImg4 from "../../../public/about/ProfileImage4.png";
import ProfileImg5 from "../../../public/about/ProfileImage5.png";

export default function ProfileSection() {
  return (
    <div className="flex -space-x-12 rtl:space-x-reverse mt-[40px]">
      <Image
        priority
        src={ProfileImg1}
        alt="shape"
        className="w-50 h-50 border-2 rounded-full dark:border-gray-800"
      />
      <Image
        priority
        src={ProfileImg2}
        alt="shape"
        className="w-50 h-50 border-2 rounded-full dark:border-gray-800"
      />
      <Image
        priority
        src={ProfileImg3}
        alt="shape"
        className="w-50 h-50 border-2 rounded-full dark:border-gray-800"
      />
      <Image
        priority
        src={ProfileImg4}
        alt="shape"
        className="w-50 h-50 border-2 rounded-full dark:border-gray-800"
      />
      <Image
        priority
        src={ProfileImg5}
        alt="shape"
        className="w-50 h-50 border-2 rounded-full dark:border-gray-800"
      />
    </div>
  );
}
