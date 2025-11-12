"use client"
import CustomSection from "./CustomSection";
import ParallaxCarousel from "./ParallaxCarousel";

const Cohorts: React.FC = () => (
  <section className=" w-full flex flex-col py-24 items-center">
    <CustomSection
      heading="COHORTS"
      description="Web 2.0 ---- Web 3.0"
    > 
     
        <h3>In Pictures</h3>
      {/**<ParallaxCarousel />*/}
    
    </CustomSection>
  </section>
);

export default Cohorts;
