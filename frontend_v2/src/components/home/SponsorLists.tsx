"use client";
import Slider from "react-slick";
import eth from "../../../public/home/eth.png";
import polygon from "../../../public/home/polygon2.png";
import hydro from "../../../public/home/hydro.png";
import Nahmi from "../../../public/home/nahmii.png";
import push from "../../../public/home/Epns.png";
import crevatal from "../../../public/home/crevatal.png";
import kernel from "../../../public/home/kernel.png";
import Sponsor from "./Sponsor";

const SponsorLists = () => {
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
        <section className="w-full h-20 dark:bg-gray-300">
            <Slider {...settings}>
                <Sponsor image={eth} />
                <Sponsor image={polygon} />
                <Sponsor image={hydro} />
                <Sponsor image={Nahmi} />
                <Sponsor image={push} />
                <Sponsor image={crevatal} />
                <Sponsor image={kernel} />
            </Slider>
        </section>
    )
}

export default SponsorLists;