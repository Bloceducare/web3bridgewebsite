"use client";
import Image from "next/image";
import Link from "next/link";

const Sponsor = ({ image, url, name }: { image: string, url: string, name: string }) => {
  return (
    <div className="px-4 ">
      <Link href={url} target="_blank" rel="noreferrer" className="block">
        <Image
          src={image}
          className="aspect-square object-contain"
          priority
          alt={name}
          width={100}
          height={100}
          quality={100}
        />
      </Link>
    </div>
  );
};

export default Sponsor;
