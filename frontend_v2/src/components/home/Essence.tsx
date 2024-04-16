"use client"
import Image from "next/image"
import Img1 from "../../../public/home/essence1.png";
import Img2 from "../../../public/home/essence2.png";
import Img3 from "../../../public/home/essence3.png";
import Slider from "react-slick";

const Essence = () => {
    // Slider settings
    const settings = {
        dots: false,
        infinite: true,
        speed: 2000,
        autoplay: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        initialSlide: 0,
    }

    return (
        <section className="w-full flex flex-col md:gap-16 gap-8 justify-center radial-gradient lg:px-6 md:px-2">
            <div className="flex flex-col gap-3 ">
                <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">Our Essence</h1>
                <p className="text-muted-foreground text-center">We are training blockchain developers in Africa</p>
            </div>
            <div className="w-full grid lg:grid-cols-2 lg:grid-rows-1 md:grid-rows-3 lg:h-[340px] md:h-[500px] h-auto rounded-lg border-2 border-bridgeRed/20 dark:border-bridgeRed/40 gap-6 lg:overflow-hidden">
                <div className="flex w-full h-full justify-center items-center md:px-8 py-6 px-6 md:py-0">
                    <p className="text-lg">We are working on building sustainable Web3 economy in Africa through remote and onsite Web3 development training, supporting web3 developers and startups, and lowering barriers of entry into the Web3 ecosystem.</p>
                </div>
                <div className="md:relative hidden md:block md:row-span-2">
                    <Image priority src={Img1} alt="image" className="absolute h-full right-0 top-0 z-[1] object-cover" />
                    <Image priority src={Img2} alt="image" className="absolute h-[80%] lg:right-[30%] md:right-[30%] rounded-t-lg bottom-0 z-[2] object-cover" />
                    <Image priority src={Img3} alt="image" className="absolute h-[60%] lg:right-[57%] md:right-[60%] rounded-t-lg bottom-0 z-[3] object-cover " />
                </div>

            </div>
            <div className="w-full h-[250px] md:hidden">
                <Slider {...settings}>
                    <div className="w-full h-[250px] px-1 rounded-lg overflow-hidden">
                        <Image src={Img1} alt="image" className="w-full  object-cover h-full object-right-top" />
                    </div>
                    <div className="w-full h-[250px] px-1 rounded-lg overflow-hidden">
                        <Image src={Img2} alt="image" className="w-full  object-cover h-full" />
                    </div>
                    <div className="w-full h-[250px] px-1 rounded-lg overflow-hidden">
                        <Image src={Img3} alt="image" className="w-full  object-cover h-full " />
                    </div>
                </Slider>
            </div>
        </section>
    )
}

export default Essence