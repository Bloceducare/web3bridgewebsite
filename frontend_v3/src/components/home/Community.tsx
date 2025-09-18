"use client";
import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";
import img1 from "../../../public/home/commnuity1.png";
import img2 from "../../../public/home/community2.png";
import img3 from "../../../public/home/community3.png";
import img4 from "../../../public/home/community4.png";
import img5 from "../../../public/home/community5.png";
import img6 from "../../../public/home/community6.png";
import img7 from "../../../public/home/community7.png";
import img8 from "../../../public/home/community8.png";
import Image from "next/image";
import { Button } from "../ui/button";
import { MoveRight } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

const images = [img1, img2, img3, img4, img5, img6, img7, img8];

const Community = () => {
  const router = useRouter();

  return (
    <section className="w-full md:my-20 my-12 flex flex-col items-center md:gap-8 gap-8 justify-center ">
      <div className="flex flex-col items-center gap-3 ">
        <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">
          The Web3Bridge Community
        </h1>
        <p className="w-full px-3 md:w-[80%] text-muted-foreground text-center">
          We love people, and people love us right back! Gain access to our ever
          growing community to connect with brilliant minds and get the needed
          support for your growth.
        </p>
      </div>

      <main className="w-full p-4 bg-gradient-to-b from-bridgeRed/50 to-bridgeRed/10">
        <ResponsiveMasonry columnsCountBreakPoints={{ 350: 2, 750: 3, 900: 4 }}>
          <Masonry gutter="16px">
            {images.map((img, index) => (
              <Image
                key={index}
                src={img}
                alt="community image"
                className="h-auto rounded-lg w-full object-cover"
                width={900}
                height={900}
                quality={100}
                priority
              />
            ))}
          </Masonry>
        </ResponsiveMasonry>
      </main>
      <Button
        onClick={() => router.push("/register")}
        className="rounded-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-bridgeRed hover:text-red-100">
        Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
      </Button>
      {/* <Link
            href="https://docs.google.com/forms/d/e/1FAIpQLScoch9kMWh4ZxkfJyl8IHTrXMGnJWwOjdk3HNpMApkXFEFP3g/viewform"
            target="_blank"
            rel="noreferrer"
            className="rounded-full flex items-center px-12 py-3.5 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed text-sm md:text-base capitalize hover:bg-bridgeRed dark:bg-bridgeRed dark:text-red-100 hover:text-red-100">
            Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
          </Link> */}
    </section>
  );
};

export default Community;
