import { Compare } from "../ui/compare";
import { CustomCards } from "./CustomCards";
import CustomSection from "./CustomSection";
//Icons
import solidity from "/public/icons/solidity.png"
import python from "/public/icons/python.png"
import rust from "/public/icons/rust.png"
import golang from "/public/icons/golang.png"
import cplusplus from "/public/icons/cplusplus.png"
import typescript from "/public/icons/typescript.png"
import javascript from "/public/icons/javascript.png"
import html5 from "/public/icons/html5.png"
import react from "/public/icons/react.png"
import mysql from "/public/icons/mysql.png"


 


const WhatWeDo: React.FC = () => (
  <section className=" flex flex-col py-24 items-center">
    <CustomSection
      heading="WHAT WE DO"
      description="We are empowering Africans to become world-class blockchain professionals."
    >
      <div className="grid grid-cols-2 gap-8 ">
        <div className="p-4 border rounded-3xl dark:bg-neutral-900 bg-neutral-100  border-neutral-200 dark:border-neutral-800 px-4">
          <Compare
        firstImage="https://assets.aceternity.com/code-problem.png"
        secondImage="https://assets.aceternity.com/code-solution.png"
        firstImageClassName="object-cover object-left-top"
        secondImageClassname="object-cover object-left-top"
        className="h-[862px] w-[545px]"
        slideMode="hover"
      />
        </div>
        <div className="grid grid-cols-1 gap-8">
          <CustomCards title="Build" description="Every line of code pushes you closer to launching real dApps. You don’t just learn — you build. Projects, portfolios, and production-level stuff." icons={[solidity.src, python.src, rust.src, golang.src, cplusplus.src]} />
           <CustomCards title="Thrive" description="You’ll join a vibrant African Web3 community that’s already shaping the future of finance, governance, and technology." icons={[typescript.src, javascript.src, html5.src, react.src, mysql.src]} />

        </div>
      </div>
    </CustomSection>
  </section>
);

export default WhatWeDo;
