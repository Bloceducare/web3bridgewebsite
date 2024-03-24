import Image, { StaticImageData } from "next/image";

import personIcon from "../../../public/dapps/pesonIcon.png"


export default function DappCard({
  description,
  title,
  image,
}: {
  description?: string;
  title?: string;
  image?: StaticImageData;
}) {
  return (
    <div className="flex">
      <div className="rounded-xl">
        <Image
          priority
          src={personIcon}
          alt="image"
          className=""
          width={100}
          height={100}
        />
      </div>
      <div className="mt-3 light:text-[#313131]">
        <h3 className="font-semibold text-2xl">
            {/* {title} */}
            Select a Compatible Wallet
            </h3>
        <p className="text-lg leading-7 mb-4 font-light">
            {/* {description} */}
        You{"'"}ll need a compatible wallet that supports the blockchain network the dApp operates on.  Download and set up your chosen wallet, ensuring you securely store your private keys.
        </p>
     
      </div>
    </div>
  );
}
