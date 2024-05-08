"use client";
import Slider from "react-slick";
import Sponsor from "./Sponsor";
import { useEffect, useState } from "react";

const SponsorLists = () => {
  const [data, setData] = useState<null | []>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/operation/partner/all/`)
      .then((res) => res.json())
      .then((data) => {
        setData(data.data);
      });
  }, []);

  const settings = {
    dots: false,
    infinite: true,
    slidesToShow: 7,
    slidesToScroll: 1,
    autoplay: true,
    speed: 3000,
    autoplaySpeed: 500,
    cssEase: "linear",
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 7,
          slidesToScroll: 1,
          infinite: true,
          dots: false,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 4,
          slidesToScroll: 1,
          initialSlide: 2,
          dots: false,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          dots: false,
        },
      },
    ],
  };

  return (
    <section className="w-full sponsor-gradient mb-24">
      <Slider {...settings}>
        {data?.map((item: any, index: number) => (
          <Sponsor
            image={item.picture}
            url={item.url}
            name={item.name}
            key={index}
          />
        ))}
      </Slider>
    </section>
  );
};

export default SponsorLists;
