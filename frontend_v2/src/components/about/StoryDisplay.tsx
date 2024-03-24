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
        description="Web3bridge is a program created in 2019 to train Web3 developers in Africa. We are working on building sustainable Web3 economy in Africa through remote and onsite Web3 development training, "
        image={StoryImage2}
        orientation="reversed"
      />

      <StorySection
        title="Where We are Headed"
        pillText="Journey Ahead"
        description="Web3bridge is a program created in 2019 to train Web3 developers in Africa. We are working on building sustainable Web3 economy in Africa through remote and onsite Web3 development training"
        image={StoryImage3}
      />
    </section>
  );
}
