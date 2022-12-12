import Button from '@components/Button'


const Golang = () => {
  
    return <>
    <div className="max-w-5xl m-12 mx-auto dark:text-white">

    <div className="w-full flex flex-wrap justify-center items-center px-7">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8">
          <h1 className="mb-8 text-3xl font-bold text-base90 dark:text-white10">
          GOLANG
          </h1>       
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10">
          This program is a 16 weeks program designed for individuals looking to further their development knowledge and become GETH developers. This program is specifically designed for existing solidity developers who want to upgrade their career and dive into protocol level development.
          </p>
        
        </div>
       
      </div>
   


      <div className="px-7 ">
      
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Golang, also known as Go, is a programming language that is specifically designed for building efficient, reliable, and scalable applications. It has quickly become a popular choice for developing blockchain solutions due to its strong emphasis on concurrency and simplicity.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        In this training, we will cover the fundamentals of Golang and how it applies to blockchain development. Topics include: </p>
       <ul className="text-base md:text-xl dark:text-[#A1A1A1] list-disc">
        <li className=" my-6 ml-5">
        Introduction to Golang and its key features
        </li>
        <li className=" my-6 ml-5">
        Setting up a development environment for Golang
        </li>
        <li className=" my-6 ml-5">
        Basics of blockchain and how it works
        </li>
        <li className=" my-6 ml-5">
        Implementing blockchain concepts in Golang
        </li>
        <li className=" my-6 ml-5">
        Building and deploying a simple blockchain application
        </li>
       </ul>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        This training is intended for existing developers who have some experience with programming and want to learn how to use Golang for building blockchain solutions. 
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        By the end of this training, you will have the knowledge and skills to start building your own blockchain applications using Golang.
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