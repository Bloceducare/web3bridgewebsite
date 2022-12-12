import Button from '@components/Button'


const Solidity = () => {
  
    return <>
    <div className="max-w-5xl m-12 mx-auto dark:text-white">

    <div className="w-full flex flex-wrap justify-center items-center px-7">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8">
          <h1 className="mb-8 text-3xl font-bold text-base90 dark:text-white10">
          SOLIDITY 
          </h1>       
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10">
          Are you an experienced developer looking to expand your skills and expertise in the world of blockchain? Our Solidity training is the perfect way to get started.
          </p>
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10 mt-4">
          This program is a 16 weeks program designed for individuals looking to further their development knowledge and become smart contract developers. This program is specifically designed for existing developers with an in-depth understanding of Javascript.
          </p>
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10 mt-4">
          This  course will help you quickly learn the fundamentals of Solidity and apply your existing knowledge to the blockchain domain.
          </p>
        
        </div>
       
      </div>
   


      <div className="px-7 ">
      
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        In this course, you'll cover topics such as:
        </p>

        
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        In this training, we will cover the fundamentals of Golang and how it applies to blockchain development. Topics include: </p>
       <ul className="text-base md:text-xl dark:text-[#A1A1A1] list-disc">
        <li className=" my-6 ml-5">
        Solidity language basics, including data types, control structures, and functions

        </li>
        <li className=" my-6 ml-5">
        Writing, testing, and deploying smart contracts with Solidity
                </li>
        <li className=" my-6 ml-5">
        Working with the Ethereum blockchain, including its EVM and gas model
        </li>
        <li className=" my-6 ml-5">
        Integrating Solidity with other tools and libraries, such as Hardhat, etherjs.
        </li>
        <li className=" my-6 ml-5">
        Advanced contract design and best practices for writing secure and efficient Solidity code
        </li>
       </ul>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Don't miss out on this exciting opportunity to gain valuable skills and advance your career. Sign up for our Solidity training today!
        </p>            
      </div>

      <Button
        href="/trainings/special-class/specialClass?type=5"
        class="py-2 px-12 mx-auto block mt-4 mb-40"
        content="Enroll Now"
        type="background"
      />
    </div>
    
    </>;
}


export default Solidity