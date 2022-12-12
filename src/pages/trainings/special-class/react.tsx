
import Button from '@components/Button'


const Reactjs = () => {  
    return <>
    <div className="max-w-5xl m-12 mx-auto dark:text-white">

    <div className=" px-7">
        <div className="px-8 md:px-0 w-full text-center md:text-left mb-8">
          <h1 className="mb-8 text-3xl font-bold text-base90 dark:text-white10">
          JAVASCRIPT, REACT, TYPESCRIPT
          </h1>       
          <p className="lg:text-xl text-base dark:text-[#A1A1A1] leading-10">
          This program is a 16 weeks program designed for individuals looking to further their development knowledge and become frontend developers. The program will cover the in-depth of Javascript, react and typescript, as it will be 100% practical and should be attended by those who already have a firm grasp of HTML and CSS.
          </p>

             
        </div>
     
      </div>
   


      <div className="px-7 ">
      
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        With JavaScript, you'll learn how to add interactivity and dynamic functionality to your web applications, making them more engaging and user-friendly. You'll also discover how to work with variables, data types, and control structures, as well as how to debug and troubleshoot your code.

        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Next, we'll dive into React, the popular JavaScript library for building user interfaces. You'll learn how to create reusable components, manage state, and perform data fetching, as well as how to integrate React with other tools and libraries.

      </p>

        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Finally, we'll cover TypeScript, a statically-typed extension of JavaScript that adds type safety and other advanced features. You'll learn how to use TypeScript to improve the quality and maintainability of your code, as well as how to integrate it with React and other tools.

        </p>
        <p className="text-base md:text-xl dark:text-[#A1A1A1] my-6">
        Don't miss out on this exciting opportunity to gain valuable skills and advance your career. Sign up for our JavaScript, React, and TypeScript training today!
        </p>      
            
      </div>

      <Button
        href="/trainings/special-class/specialClass?type=2"
        class="py-2 px-12 mx-auto block mt-4 mb-40"
        content="Enroll Now"
        type="background"
      />
    </div>
    
    </>;
}


export default Reactjs