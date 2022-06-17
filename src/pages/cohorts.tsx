import Image from "next/image";
import CohortsImage from "../../assests/cohorts/cohorts.svg";
import ProfileImg from "../../assests/cohorts/profile.svg";
import Button from "../components/Button";

const Cohorts = () => {
  return (
    <section className="py-4">
      <div className="w-full flex justify-center ">
        <div className="w-[30%]  self-end">
          <h1 className="text-white10 font-bold text-3xl mb-4">
            Cohort Explainer
          </h1>
          <p className="text-[#A1A1A1] py-3 text-xl">
            Do you want to build for the the blockchain?
          </p>
          <p className="text-[#A1A1A1] py-3 text-xl">
            Do you desire to land a good paying job?
          </p>
          <p className="text-[#A1A1A1] py-3 text-xl">
            Do you desire to upgrade from trenches?
          </p>
          <p className="text-[#A1A1A1] py-3 text-xl">
            and you don’t know how to go about this?.
          </p>
        </div>
        <div className="w-[40%]  ">
          <Image src={CohortsImage} />
        </div>
      </div>
      <p className=" ml-[12.5rem] text-xl text-[#A1A1A1]">
        worry no more because Web3bridge can make this desires a reality.
      </p>
      <div className="px-[12rem]">
        <h2 className="text-white10 mt-[5rem] font-bold mb-10 text-2xl">
          How?
        </h2>
        <p className="text-[#A1A1A1] my-6">
          Web3bridge runs a 16weeks cohort based training that will hold you by
          the hand to give you the right head start to launch your Blockchain
          Development as we help navigate you from the state of the known to the
          fiery edge of the unknown.
        </p>
        <p className="text-[#A1A1A1] my-6">
          Within this 16weeks you are going to give you an immersive learning
          experience on what it takes to be a Blockchain Developer and we are
          not just going to develop your technical skills but also help build
          your soft skills to be able to compete in the global market.
        </p>
        <p className="text-[#A1A1A1] my-6">
          Graduates from our program have gone to work with global brands such
          as Aavegotchi, Consensys, Nahmii, Nethermind, Polygon and lots more.
          So be rest assured that you are going to have the best learning
          experience with our program.
        </p>
      </div>
      <div className="w-ful flex items-center justify-center mt-16">
        <Image src={ProfileImg} />
        <p className="text-white10">230+ Students enrolled</p>
      </div>
      <Button class="py-2 px-12 mx-auto block mt-4 mb-40" content="Enroll Now" type="background" />
    </section>
  );
};

export default Cohorts;
