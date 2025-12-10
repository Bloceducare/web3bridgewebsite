import Image from "next/image";
import CustomSection from "./CustomSection";
import { InfiniteMovingCards } from "../ui/infinite-moving-cards";
import testimonialsData from "@/data/testimonials";



const Alumni: React.FC = () => (
  <section className=" w-full flex flex-col py-24 items-center">
    <CustomSection
      heading="alumni"
      description="Our students have these to say..."
    > 

      
        <InfiniteMovingCards items={testimonialsData} speed="slow" />
    
     
    </CustomSection>
  </section>
);

export default Alumni;
