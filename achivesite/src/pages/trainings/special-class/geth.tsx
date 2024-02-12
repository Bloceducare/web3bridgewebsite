import Button from '@components/Button'


const Golang = () => {
  
    return <>
    <div className="max-w-5xl m-12 mx-auto dark:text-white">

    <div className="w-full flex flex-wrap justify-center items-center px-7">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8">
          <h1 className="mb-8 text-3xl font-bold text-base90 dark:text-white10">
          GETH
          </h1>       
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10">
          This program is a 16 weeks program designed for individuals looking to further their development knowledge and become GETH developers. This program is specifically designed for existing solidity developers who want to upgrade their career and dive into protocol level development.
          </p>
        
        </div>
       
      </div>
   


      <div className="px-7 ">
      
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Geth has been a crucial part of Ethereum from the start. It's one of the earliest versions of Ethereum, so it's been thoroughly tried and tested.
        </p>

        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Think of Geth as the worker that manages things on the Ethereum network. It takes care of tasks like processing transactions, setting up and running smart contracts, and it even has a built-in computer called the Ethereum Virtual Machine.
        </p>

        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        In this training, we will cover the fundamentals of Geth and how it applies to blockchain development. Topics include: </p>
       <ul className="text-base md:text-xl dark:text-[#A1A1A1] list-disc">
        <li className=" my-6 ml-5">
        Introduction to Go-ethereum and its key features
        </li>
        <li className=" my-6 ml-5">
        Setting up and running a node
        </li>
        <li className=" my-6 ml-5">
        Basics of blockchain and how it works
        </li>
        <li className=" my-6 ml-5">
        Implementing blockchain concepts in Golang
        </li>
        <li className=" my-6 ml-5">
        Building and deploying a blockchain applications
        </li>
       </ul>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        This training is intended for existing developers who have some experience with programming and want to learn how to use Golang for building blockchain solutions. 
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        By the end of this training, you will have the knowledge and skills to setup and run a full Ethereum nodes, Be a competent Validator and a path to become a protocol engineer
        </p>
      
      </div>

      <Button
        href="/trainings/special-class/specialClass?type=4"
        class="py-2 px-12 mx-auto block mt-4 mb-40"
        content="Enroll Now"
        type="background"
      />
    </div>
    
    </>;
}


export default Golang