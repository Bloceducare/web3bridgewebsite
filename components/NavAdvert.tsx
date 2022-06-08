import Arrow from "../assests/about-us/arrow.svg"
import Image from "next/image"
const NavAdvert = () => {
  return (
    <div className="w-full bg-[#111111] dark:bg-[#FA0101] text-center text-white text-sm py-4 flex items-center justify-center">
      <p className="mr-4">
        🎉 Free: Registration for the cohort VII currently ongoing Apple {" "}
        <span>
          <a className="underline text-[#737373]" href="">here</a>
        </span>
      </p>
        <Image src={Arrow} />
    </div>
  );
};

export default NavAdvert;
