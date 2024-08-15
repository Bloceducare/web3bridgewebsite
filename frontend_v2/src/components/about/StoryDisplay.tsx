import StorySection from "./StorySection";
import StoryImage1 from "../../../public/about/StoryImage1.png";
import StoryImage2 from "../../../public/about/StoryImage2.png";
import StoryImage3 from "../../../public/about/StoryImage3.png";

export default function StoryDisplay() {
  return (
    <section className="w-full flex flex-col mt-8 gap-1 md:gap-10 justify-center md:px-16 md:py-20 py-10 radial-gradient ">
      <StorySection
        title="Where We Started from"
        pillText="Our Journey"
        description="Web3bridge is a program created in 2019 to train Web3 developers in Africa. We are working on building sustainable Web3 economy in Africa through remote and onsite Web3 development training"
        image={StoryImage1}
      />

      <StorySection
        title="Where We are"
        pillText="Right Here, Right Now"
        description="We have made true to our plans to train Web3 developers across Africa, and we have trained over a thousand (1000) developers directly and indirectly through our Web3, Web2 cohorts and masterclasses. 

Our commitment and consistency has also made us the choice partner for protocols and projects looking to train and hire developers from Africa.

Since we moved to the hybrid training program, we have expanded our facilities to be able to house up to two hundred (200) developers and halls to accommodate the same."
        image={StoryImage2}
        orientation="reversed"
      />

      <StorySection
        title="Where We are Headed"
        pillText="Journey Ahead"
        description="Our journey is such that keeps unveiling as we grow, however, we are confident in becoming one of the biggest Web3 training providers in the entire continent of Africa, training and grooming developers in their numbers, partnering with protocols and projects, and supporting new training initiatives, programs and companies springing up across the African continent.
"
        image={StoryImage3}
      />
    </section>
  );
}
