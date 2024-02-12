import Link from "next/link";
import Image from "next/image";
import Button from '@components/Button'


const Golang = () => {
  
    return <>
    <div className="max-w-5xl m-12 mx-auto dark:text-white">

    <div className="w-full flex flex-wrap justify-center items-center xl:px-[10rem]">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8 md:w-[40%] lg:w-[50%] xl:w-[40%]">
          <h1 className="mb-8 text-3xl font-bold text-base90 dark:text-white10">
          HTML, CSS, INTRO TO JAVASCRIPT
          </h1>       
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10">
          This program is a 12 weeks program designed for individuals who are just about to kick start their journey into becoming a developer.
          </p>

          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10 mt-4">
          Our instructors will guide you through the basics of these essential languages, giving you the knowledge and confidence you need to succeed in today's competitive job market.
          </p>
       
        </div>
        <div className="w-[80%] md:w-[40%] md:ml-10 lg:m=l-0 ">
          <Image
          width={800}
          height={800}
           src="/html-css-js.svg" />
        </div>
      </div>
   


      <div className="px-7 ">
      
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        With JavaScript, you'll learn how to add interactivity and dynamic functionality to your websites, making them more engaging and user-friendly. You'll also discover how to work with variables, data types, and control structures, as well as how to debug and troubleshoot your code.
        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Next, we'll dive into CSS, the language that controls the presentation and styling of your web pages. You'll learn how to use CSS to create beautiful and responsive layouts, as well as how to work with colors, fonts, and other design elements.
      </p>

        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Finally, we'll cover HTML, the foundation of all web pages. You'll learn how to structure and organize your content, as well as how to add images, videos, and other multimedia elements to your pages.

        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Don't miss out on this exciting opportunity to gain valuable skills and advance your career. Sign up for our JavaScript, CSS, and HTML fundamentals training today!
        </p>      
      </div>

      <Button
        href="/trainings/special-class/specialClass?type=1"
        class="py-2 px-12 mx-auto block mt-4 mb-40"
        content="Enroll Now"
        type="background"
      />
    </div>
    
    </>;
}


export default Golang