import Image, { StaticImageData } from "next/image";
import StoryImage1 from "../../../public/about/StoryImage1.png";
import Pill from "../shared/pill";

export default function StorySection({pillText, title, description, orientation, image}:{pillText:string, title:string, description:string, orientation?:string, image:StaticImageData }) {
  return (
    
      <main className="w-full flex lg:flex-row flex-col gap-4 md:gap-10 justify-between items-center py-6">
        <div className={`basis-1/2 light:text-[#1B1B1B] order-first ${orientation === 'reversed' ? 'lg:order-last' : 'order-first'}`}>
          <Pill text={pillText}/>
          <h1 className="mb-4 mt-2 md:mt-5 text-xl md:text-4xl font-semibold leading-none tracking-tight">
            {/* Where We Started from */}
            {title}
          </h1>
          <p className="mb-2 font-light leading-12  lg:mb-8 md:text-xl text-md lg:text-xl">
            {description}
          </p>
        </div>

        <div className="">
          <Image priority src={image} alt="Story image" className="" />
        </div>
      </main>
    
  );
}
