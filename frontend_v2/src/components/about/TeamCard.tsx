import Image from "next/image";
import Team1 from "../../../public/about/Team1.png";

export default function TeamCard({
  name,
  role,
  image,
}: {
  name: string;
  role: string;
  image: string;
}) {
  return (
    <div className="w-[296px] bg-gradient-to-b from-red-100 to-background rounded-xl border-2 drop-shadow-[rgba(255, 214, 214, 0.24)] p-[32px]">
      <div>
        <Image
          priority
          src={image}
          alt="Story image"
          className=""
          width={230}
          height={230}
        />
      </div>
      <div className="mt-3 text-[#1B1B1B]">
        <h3 className="font-semibold text-lg leading-6 mb-1">{name}</h3>
        <p className="text-sm leading-7 text-light">{role}</p>
      </div>
    </div>
  );
}
