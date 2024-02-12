import Link from "next/link";
import Image from "next/image";
import Button from '@components/Button'


const Nodejs = () => {  
    return <>
    <div className="max-w-5xl m-12 mx-auto dark:text-white">

    <div className=" px-7">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8">
          <h1 className="mb-8 text-3xl font-bold text-base90 dark:text-white10">
          JAVASCRIPT, NODEJS
          </h1>       
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10">
          This program is a 16 weeks program designed for individuals looking to further their development knowledge and become backend developers. The program will cover the indepth of Javascript and NodeJS as it will be 100% practical and should be attended by those who already have a firm grasp of HTML and CSS.
          </p>

             
        </div>
     
      </div>
   


      <div className="px-7 ">
      
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Our instructors will guide you through the basics of these essential technologies, giving you the knowledge and confidence you need to succeed in today's competitive job market.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        With Node.js, you'll learn how to create efficient and scalable server-side applications using JavaScript. You'll also discover how to work with popular Node.js frameworks and libraries, such as Express.

      </p>

        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Next, we'll dive into Express, the most popular web framework for Node.js. You'll learn how to use Express to create RESTful APIs and web applications, as well as how to integrate it with other tools and libraries.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Then, we'll cover MongoDB, the most popular NoSQL database. You'll learn how to use MongoDB to store and manage data for your Node.js applications, as well as how to work with Mongoose, the popular MongoDB object modeling tool.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Finally, we'll cover REST APIs, the standard architecture for building web services. You'll learn how to design and implement RESTful APIs, authentication, authorization as well as how to test and deploy them to the web.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Don't miss out on this exciting opportunity to gain valuable skills and advance your career. Sign up for our Node.js, Express, MongoDB, and REST API training today!

        </p>      
      </div>

      <Button
        href="/trainings/special-class/specialClass?type=3"
        class="py-2 px-12 mx-auto block mt-4 mb-40"
        content="Enroll Now"
        type="background"
      />
    </div>
    
    </>;
}


export default Nodejs