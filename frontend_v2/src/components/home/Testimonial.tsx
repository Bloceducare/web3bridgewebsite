"use client";
import { useRef } from "react";
import TestimonialCard from "./TestimonialCard";
import Slider from "react-slick";
import { Button } from "../ui/button";
import { CaretLeftIcon, CaretRightIcon } from "@radix-ui/react-icons";
import testimonialsData from "@/data/testimonials";

const Testimonial = () => {
  const sliderRef = useRef<Slider | null>();

  // Function for next button
  const next = () => {
    if (sliderRef.current) {
      sliderRef.current.slickNext();
    }
  };
  // function for previous button
  const previous = () => {
    if (sliderRef.current) {
      sliderRef.current.slickPrev();
    }
  };

  // Slider settings
  const settings = {
    dots: false,
    infinite: true,
    speed: 2000,
    // autoplay: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    initialSlide: 0,
    arrow: false,
    // nextArrow: "",
    // prevArrow: "",
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          infinite: true,
          dots: false,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          initialSlide: 2,
          dots: false,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          dots: false,
        },
      },
    ],
  };

  return (
    <section className="w-full h-auto flex flex-col gap-3 items-center md:mt-24">
      <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">
        Stories From Our Students
      </h1>
      <p className="lg:w-[30%] md:w-[70%] w-full text-muted-foreground text-center">
        All around the world, our students are exceptional. See what they have
        to say
      </p>
      <main className="w-full lg:px-12 px-2 mt-6">
        <Slider ref={(slider) => (sliderRef.current = slider)} {...settings}>
          {testimonialsData.map((data, i) => (
            <TestimonialCard
              key={i}
              title={data.title}
              description={data.description}
              user={data.user}
              role={data.role}
              image={data.image}
            />
          ))}
        </Slider>
      </main>
      {/* Controllers  */}
      <div className="lg:mt-6 mt-4 w-full flex justify-center gap-5 items-center md:px-6 px-3">
        <Button
          onClick={previous}
          className="rounded-lg px-4 py-4 border-2 ring-2 ring-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-bridgeRed hover:text-red-100 dark:bg-bridgeRed dark:text-red-100"
          type="button"
        >
          <CaretLeftIcon className="w-6 h-6" />
        </Button>
        <Button
          onClick={next}
          className="rounded-lg px-4 py-4 border-2 ring-2 ring-red-300 bg-red-500/10 text-bridgeRed capitalize hover:bg-bridgeRed hover:text-red-100 dark:bg-bridgeRed dark:text-red-100"
          type="button"
        >
          <CaretRightIcon className="w-6 h-6" />
        </Button>
      </div>
    </section>
  );
};

export default Testimonial;
