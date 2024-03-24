import Image, { StaticImageData } from "next/image";
import defi from "../../../public/dapps/defi.png";
import gaming from "../../../public/dapps/gaming.png";

import Pill from "../shared/pill";

export default function HeroSection() {
  return (
    <main>
      <div className="w-full flex lg:flex-row flex-col gap-4 md:gap-10 justify-between items-center py-6">
        <div className={`basis-1/2 text-[#1B1B1B] order-first`}>
          <Pill text="Decentralized Networks" />
          <h1 className="mb-4 mt-2 md:mt-5 text-xl md:text-4xl font-semibold leading-none tracking-tight">
            {/* Where We Started from */}
            Building for Your Web3 Journey!
          </h1>
          <p className="mb-2 font-light leading-12  lg:mb-8 md:text-xl text-md lg:text-2xl">
            Dapps are a growing movement of applications that use Ethereum to
            disrupt business models or invent new ones.
          </p>
          <div className="flex mr-3">
            <span className="flex items-center">
              <Image priority src={defi} alt="defi" className="mr-2" />{" "}
              Decentralized Finance
            </span>
            <span className="flex items-center">
              <Image priority src={gaming} alt="gaming" className="mr-2" />{" "}
              Gaming
            </span>
            <span className="flex items-center">
              <Image priority src={defi} alt="defi" className="mr-2" />{" "}
              Art and Collectibles
            </span>
          </div>
        </div>

        <div className="">
          {/* <Image priority src={image} alt="Story image" className="" /> */}
        </div>
      </div>
    </main>
  );
}
