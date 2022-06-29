import React from 'react'
import { Testimonials } from '../Data'

const Testimonial = () => {
  return (
    <div className="flex flex-col items-center justify-center  mt-20 ">
      <div className="flex flex-col items-center justify-center">
<<<<<<< HEAD
        <h1 className=" text-base font-secondary mt-10 mb-6 text-2xl font-bold text-center md:mt-0 md:text-5xl ">
=======
        <h1 className=" text-base dark:text-white10 font-secondary  mb-6 text-2xl font-bold text-center md:mt-0 md:text-5xl ">
>>>>>>> fb8e348bfa984b889fc46e65ac60720dea71d0ae
          What our students say
        </h1>
        <p className=" w-11/12  m-2/5 mb-20 text-base text-center text-white60 md:w-4/5 ">
          Hear from our students narrates how their experience has been before
          and after coming across our program
        </p>
      </div>
      <div className="w-full flex flex-col-reverse  justify-around mt-10 md:flex-row dark:bg-base md:w-10/12">
        {Testimonials.map((testimonial, index) => {
          return (
            <div
              key={index}
              className=" 3/12 bg-white dark:bg-base p-5 m-3 shadow-2xl rounded-md"
            >
              <p className="w-full p-2 font-secondary text-base text-white60 dark:text-white20 mb-1 md:w-full">
                {testimonial.text}
              </p>
              <div className="flex items-center ">
<<<<<<< HEAD
                <div className="w-12 h-12">
                  <img src={testimonial.image} alt="testimonial image" />
=======
                <div className="">
                  <img
                    className="w-14 h-14 rounded-full "
                    src={testimonial.image}
                    alt="testimonial image"
                  />
>>>>>>> fb8e348bfa984b889fc46e65ac60720dea71d0ae
                </div>
                <div className=" ml-4">
                  <p className="text-primary font-semibold font-secondary text-xl ">
                    {testimonial.name}
                  </p>
<<<<<<< HEAD
                  <p className="font-secondary text-base, text-white60 ">
=======
                  <p className="font-secondary text-base, text-white60 dark:text-white20 ">
>>>>>>> fb8e348bfa984b889fc46e65ac60720dea71d0ae
                    {testimonial.position}
                  </p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Testimonial
