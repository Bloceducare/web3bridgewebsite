import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import Button from "@components/commons/Button";


const courseLinks = [
  {
 link:"/trainings/special-class/specialClass?type=1",
 label:"Html, CSS Javascript Intro"
},
  {
 link:"/trainings/special-class/specialClass?type=2",
 label:"Javascript, React, Typescript "
},
  {
 link:"/trainings/special-class/specialClass?type=3",
 label:"Javascript, Nodejs "
},
  {
 link:"/trainings/special-class/specialClass?type=4",
 label:"GETH "
},
  {
 link:"/trainings/special-class/specialClass?type=5",
 label:"Solidity"
},
 
]
const SpecializedClass = () => {

  const [showModal, setShowModal] = useState(false);

  useEffect(()=>{
    if(showModal){
      document.body.style.overflow="hidden"     
    }

    return ()=>{
      document.body.style.overflow="auto"
    }
    
  },[showModal])

    return <>
      {showModal ? (
        <>
          <div
            className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none dark:text-white10  bg-white dark:bg-base90 transition-all"
          >
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              {/*content*/}
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full outline-none focus:outline-none">
                {/*header*/}
                <div className="flex items-start justify-between p-5 border-b border-solid border-slate-200 rounded-t">
                  <h3 className="text-2xl font-semibold">
                  Pick a Course
                  </h3>

                  <button
                    className="p-1 ml-auto bg-trnsparent border-0 text-red-500 opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                    onClick={() => setShowModal(false)}
                  >
                    <span className="bg-transparent text-red-500 opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">
                      ×
                    </span>
                  </button>
                  <button className="text-2xl dark:text-white"  onClick={() => setShowModal(false)}>
                  ×

                  </button>
                </div>
                {/*body*/}
                <div className="relative p-6 flex-auto">
                  {
                    courseLinks.map((item, id)=>(
                      <div className="my-4  text-lg  block w-screen max-w-xl">

<span className="link-wrapper">
      
         
                    <Link key={id} href={item.link}>
                      <a className="">     

                      {item.label}    
        </a>
            
                     
                    </Link>
                    </span>
                    </div>
                    ))
                  }
               
                </div>            
              </div>
            </div>
          </div>
        </>
      ) : null}
    <div className="max-w-5xl m-12 mx-auto dark:text-white">

    <div className="w-full flex flex-wrap justify-center items-center xl:px-[10rem]">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8 md:w-[40%] lg:w-[50%] xl:w-[40%]">
          <h1 className="mb-8 text-3xl font-bold text-base90 dark:text-white10">
          The Web3bridge specialized class
          </h1>       
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10">
          The Web3Bridge  specialized, paid, on-demand class offers a flexible learning schedule, allowing you to choose between morning and evening classes
          </p>
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10 mt-4">
         Plus, with a range of course options to choose from, you can find the perfect fit for your goals and interests.
          </p>
        </div>
        <div className="w-[80%] md:w-[40%] md:ml-10 lg:m=l-0 ">
          <Image
          width={800}
          height={800}
           src="/programming.svg" />
        </div>
      </div>
   


      <div className="px-7 ">
      
        <p className=" text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Our course offerings include {" "}
        <Link href="/trainings/special-class/html-css">
          <span className="link-wrapper">
        <a className="">
        HTML, CSS, and JavaScript fundamentals
        </a>

          </span>
         
        </Link>
        {" "}
          giving you a strong foundation in web development. You'll learn how to structure and style web pages, as well as how to add interactivity and dynamic functionality with JavaScript.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        We also offer courses in advanced JavaScript, including 
        <Link href="/trainings/special-class/nodejs">
          <span className="link-wrapper">
        <a className=""> Node.js
        </a>
          </span>
         
        </Link>
        {" "} and  {" "}
        
        <Link href="/trainings/special-class/react">
          <span className="link-wrapper">
        <a className="">
        React.js with TypeScript
        </a>

          </span>
         
        </Link> {" "}

        . These courses will help you build scalable, efficient, and modern web applications, using cutting-edge technologies and best practices. </p>

        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        In addition to web development, we also offer courses in 
        { " "} 

        <Link href="/trainings/special-class/solidity">
          <span className="link-wrapper">
        <a className="">
        Solidity
        </a>

          </span>
         
        </Link>
         {" "}
       , the language of the Ethereum blockchain, and {" "}
       
       <Link href="/trainings/special-class/geth">
          <span className="link-wrapper">
        <a className="">
        Go-ethereum
        </a>

          </span>
         
        </Link>

       {" "}
       , Official Golang implementation of the Ethereum protocol
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Throughout our courses, you'll have plenty of opportunities to practice what you've learned through hands-on exercises and projects. You'll also receive personalized feedback and support from our instructors, ensuring that you stay on track and make the most of your learning experience.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Don't miss out on this exciting opportunity to gain valuable skills and advance your career. Sign up for our specialized, paid, on-demand class today!
        </p>
      </div>



{/* <Button */}

<div className="flex justify-center">

<Button  
type="button" 
className="px-10"
onClick={() => setShowModal(true)}>
 Enroll
</Button>
</div>    
    </div>
    
    </>;
}


export default SpecializedClass