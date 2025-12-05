"use client"

import Link from "next/link"
import CustomSection from "./CustomSection";
import ParallaxCarousel from "./ParallaxCarousel";
import { carouselImages } from "@/data/carouselImages";
import { buttonVariants } from "../ui/button";
const Cohorts: React.FC = () => (
  <section className=" w-full flex flex-col py-24 items-center">
    <CustomSection
      heading="COHORTS"
      description="Web 2.0 ---- Web 3.0"
    >

      <div className="mt-4 mb-8">
        <h3 className="text-center">In Pictures</h3>
        <ParallaxCarousel images={carouselImages} />

      </div>

    </CustomSection>
    <Link
      href={"/register"}
      className={buttonVariants({
        variant: "bridgePrimary",
      })}
    >
      Join the next cohort
    </Link>

  </section >
);

export default Cohorts;
