const Pill = ({ text }: { text: string }) => {
  return (
    <button
      type="button"
      className="w-fit text-center text-xs md:text-sm lg:text-base text-bridgeRed font-normal bg-[linear-gradient(180deg,_#ff020233_0%,_#fb3e3e00_100%)] rounded-full px-5 py-2.5 me-2 mb-2">
      {text}
    </button>
  );
};

export default Pill;
