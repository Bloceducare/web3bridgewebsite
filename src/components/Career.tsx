import React from 'react'
import { web3Courses, web2Courses } from 'data'
import { motion } from 'framer-motion'

const Career = () => {
  return (
    <div className="flex flex-col items-center justify-center w-full mt-24">
      <div className="w-5/6 ">
        <h1 className="mb-6 text-base text-xl font-semibold text-center font-secondary dark:text-white10 md:text-4xl ">
          Change your life and start your career in web 3
        </h1>
        <p className="text-xl text-center font-primary text-white60 ">
          Get all the needed support you need to launch your web3 career with
          web3bridge.
        </p>
      </div>
      <div className="flex flex-col-reverse justify-around w-11/12 mt-20 md:w md:flex-row">
        <div className="w-full  md:w-2/5">
          <h2 className="mb-10 text-2xl font-semibold text-center text-base90 dark:text-white10 mt-7 font-secondary md:text-4xl">
            Web 3 Cohort ongoing
          </h2>
          <p className="mb-10 text-xl font-normal font-primary text-white60">
            Get everything you need to launch your career in Blockchain
            Development through our trainings that gives you the nitty gritty of
            experience through practical classes.
          </p>
          <div className="">
            <p className="flex items-center mb-5">
              <img src="./star.PNG" alt="star bullet" />
              <span className="font-primary font-normal, text-white50 text-xl ml-3 ">
                5/5 - 100% Completion rate
              </span>
            </p>
            <p className="font-primary font-normal, text-white50 text-xl mb-7">
              Full Time: 4 Months
            </p>
            <p className="flex items-center mb-7">
              <img src="./location.PNG" alt="location" />
              <span className="font-primary font-normal, text-white50 text-xl ml-3 ">
                Onsite and Virtual
              </span>
            </p>
          </div>
          <div className="flex flex-wrap w-full md:w-full xl:w-2/4">
            {web3Courses.map((course, index) => {
              return (
                <div key={index} className="">
                  <p className="flex items-center mr-5 mb-7 ">
                    <img src={course.bullet} alt="star bullet" />
                    <span className="font-primary font-normal, text-base dark:text-white20 ml-2 ">
                      {course.courseTitle}
                    </span>
                  </p>
                </div>
              )
            })}
          </div>
          <div className="mt-10 ">
            <motion.button
              whileTap={{ scale: 0.3 }}
              transition={{ duration: 0.4 }}
              className="py-2 text-base border-2  px-7 border-base dark:border-white20 text-base90 dark:text-white20 font-secondary md:py-4 md:px-14"
            >
              View Cohort
            </motion.button>
          </div>
        </div>
        <div className="w-full  md:w-5/12">
          <img className="w-full" src="./hero1.png" alt="web3 cohort Image" />
        </div>
        {/* web 2 Cohort */}
      </div>
      <div className="flex flex-col-reverse justify-around w-11/12 mt-10 md:flex-row">
        <div className="w-full  md:w-5/12">
          <img
            className="w-full"
            src="./web2cohort.png"
            alt="web3 cohort Image"
          />
        </div>

        <div className="w-full  md:w-2/5">
          <h2 className="mb-10 text-2xl font-semibold text-center text-base90 dark:text-white10 mt-7 font-secondary md:text-4xl">
            Web 2 Cohort ongoing now!
          </h2>
          <p className="mb-10 font-normal font-primary md:text-xl text-white60">
            Want to get started in coding but don’t know where to start, You can
            get all the needed trainings to make you a proficient Web Developer
            through our 6 months hands-on training on web2 technologies.
          </p>
          <div className="">
            <p className="flex items-center mb-5">
              <img src="./star.PNG" alt="star bullet" />
              <span className="font-primary font-normal, text-white50 text-xl ml-3 ">
                5/5 - 100% Completion rate
              </span>
            </p>
            <p className="font-primary font-normal, text-white50 text-xl mb-7">
              Full Time: 23 weeks
            </p>
            <p className="flex items-center mb-7">
              <img src="./location.PNG" alt="location" />
              <span className="font-primary font-normal, text-white50 text-xl ml-3 ">
                Strictly Virtual
              </span>
            </p>
          </div>
          <div className="flex flex-wrap w-full  md:w-full xl:w-2/4">
            {web2Courses.map((course, index) => {
              return (
                <div key={index} className="">
                  <p className="flex items-center mr-5 mb-7 ">
                    <img src={course.bullet} alt="star bullet" />
                    <span className="font-primary font-normal, text-base dark:text-white20 ml-2 ">
                      {course.courseTitle}
                    </span>
                  </p>
                </div>
              )
            })}
          </div>
          <div className="my-10 ">
            <motion.button
              whileTap={{ scale: 0.3 }}
              transition={{ duration: 0.4 }}
              className="py-2 text-base border-2 px-7 border-base dark:border-white20 text-base90 dark:text-white20 font-secondary md:py-4 md:px-14"
            >
              View Cohort
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Career
