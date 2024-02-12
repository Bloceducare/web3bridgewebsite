import React from 'react'
import { Testimonials } from 'data'

const Testimonial = () => {
  return (
    <div className="flex flex-col items-center justify-center mt-20 ">
      <div className="flex flex-col items-center justify-center">
        <h1 className="mb-6 text-base text-2xl font-bold text-center  dark:text-white10 font-secondary md:mt-0 md:text-5xl">
          What our students say
        </h1>
        <p className="w-11/12 mb-20 text-base text-center  m-2/5 text-white60 md:w-4/5">
          Hear from our students narrates how their experience has been before
          and after coming across our program.
        </p>
      </div>
      <div className="flex flex-col-reverse justify-around w-full mt-10 md:flex-row dark:bg-base md:w-10/12">
        {Testimonials.map((testimonial, index) => {
          return (
            <div
              key={index}
              className="p-5 m-3 bg-white rounded-md shadow-2xl  3/12 dark:bg-base md:w-10/12"
            >
              <p className="w-full p-2 mb-1 text-base font-secondary text-white60 dark:text-white20 md:w-11/12">
                {testimonial.text}
              </p>
              <div className="flex items-center ">
                <div className="">
                  <img
                    className="rounded-full w-14 h-14 "
                    src={testimonial.image}
                    alt="testimonial image"
                  />
                </div>
                <div className="ml-4 ">
                  <p className="text-xl font-semibold text-primary font-secondary ">
                    {testimonial.name}
                  </p>
                  <p className="font-secondary text-base, text-white60 dark:text-white20 ">
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
