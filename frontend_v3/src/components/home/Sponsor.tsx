"use client";
import Image from "next/image";
import Link from "next/link";

const Sponsor = ({ image, url, name }: { image: string, url: string, name: string }) => {
  const image_link = `https://res.cloudinary.com/dvuwy2tny/image/upload/${image}`;

  return (
    <div className="px-4 ">
      <Link href={url} target="_blank" rel="noreferrer" className="block">
        <Image
          src={image_link}
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
