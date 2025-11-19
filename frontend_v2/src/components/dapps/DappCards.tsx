import Image, { StaticImageData } from "next/image";
import Link from "next/link";

import { Button } from "../ui/button";

export default function DappCard({
  description,
  buttonText,
  image,
  link,
}: {
  description: string;
  buttonText: string;
  image: StaticImageData;
  link?: string;
}) {
  const buttonContent = (
    <Button className="w-full sm:w-auto rounded-full px-6 sm:px-8 md:px-12 py-4 sm:py-5 md:py-6 text-sm sm:text-base border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed hover:bg-transparent">
      {buttonText}
    </Button>
  );

  return (
    <div className="w-full max-w-[405px] mx-auto h-full min-h-[600px] sm:min-h-[650px] flex flex-col">
      <div className="w-full flex-shrink-0">
        <Image
          priority
          src={image}
          alt="Story image"
          className="rounded-2xl w-full h-full object-cover"
          placeholder="blur"
        />
      </div>
      <div className="mt-3 sm:mt-4 light:text-[#313131] flex flex-col  gap-8">
        <p className="text-sm sm:text-base md:text-lg leading-6 sm:leading-7 sm:mb-4 font-light flex-grow">
          {description}
        </p>
        <div className="flex justify-center sm:justify-start mt-auto">
          {link && link !== "/" ? (
            <Link href={link} target="_blank" rel="noopener noreferrer" className="w-full sm:w-auto">
              {buttonContent}
            </Link>
          ) : (
            <div className="w-full sm:w-auto">{buttonContent}</div>
          )}
        </div>
      </div>
    </div>
  );
}
