import Image from "next/image";

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
    <div className="w-[296px] bg-gradient-to-b from-red-100 to-background rounded-xl border-2 drop-shadow-[0_4px_6px_rgba(255,214,214,0.24)] p-6">
      <div className="relative w-full aspect-square mb-4">
        <Image
          priority
          src={image}
          alt={`${name}'s profile picture`}
          className="rounded-md object-cover"
          layout="fill"
        />
      </div>
      <div className="light:text-[#1B1B1B] text-center">
        <h3 className="font-semibold text-base leading-6 mb-1">{name}</h3>
        <p className="text-sm text-gray-700 dark:text-white leading-7 text-light">
          {role}
        </p>
      </div>
    </div>
  );
}
