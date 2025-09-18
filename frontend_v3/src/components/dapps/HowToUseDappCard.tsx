import Image, { StaticImageData } from "next/image";

import personIcon from "../../../public/dapps/pesonIcon.png";


export default function HowToUseDappCard({
  description,
  title,
  image,
}: {
  description?: string;
  title?: string;
  image: StaticImageData;
}) {
  return (
    <div className="flex gap-4 sm:px-4 md:px-0 md:gap-8 w-fit">
      {/* <div className="rounded-xl"> */}
        <Image
          priority
          src={image}
          alt="image"
          className="md:w-[80px] md:h-[80px] w-[40px] h-[40px]"
          width={100}
          height={100}
        />
      {/* </div> */}
      <div className="light:text-[#313131] md:max-w-[400px]">
        <h3 className="font-semibold text-xl md:text-2xl">
            {title}
            {/* Select a Compatible Wallet */}
            </h3>
        <p className="text-md md:text-lg leading-7 mb-4 font-light">
            {description}
        {/* You{"'"}ll need a compatible wallet that supports the blockchain network the dApp operates on.  Download and set up your chosen wallet, ensuring you securely store your private keys. */}
        </p>
     
      </div>
    </div>
  );
}
