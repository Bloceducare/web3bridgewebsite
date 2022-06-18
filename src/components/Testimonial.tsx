import React from 'react'
import { Testimonials } from '../Data'

const Testimonial = () => {
  return (
    <div className="flex flex-col items-center justify-center  mt-20 ">
      <div className="flex flex-col items-center justify-center">
        <h1 className=" text-base font-secondary mt-10 mb-6 text-2xl font-bold text-center md:mt-0 md:text-5xl ">
          What our students say
        </h1>
        <p className=" w-11/12  m-2/5 mb-20 text-base text-center text-white60 md:w-4/5 ">
          Consectetur sit lacinia odio sed egestas. Habitant ornare risus donec
          tristique lobortis egestas amet. In aenean in ut risus pulvinar vitae
          erat mattis sit fusce ac quisque suspendisse.
        </p>
      </div>
      <div className="w-full flex flex-col-reverse  justify-around mt-10 md:flex-row bg-background10 md:w-10/12">
        {Testimonials.map((testimonial, index) => {
          return (
<<<<<<< HEAD
            <div className=" 3/12 bg-white p-5 m-3">
              <p className="w-full p-2 font-secondary text-base text-white60 mb-1 md:w-full">
=======
            <div
              key={index}
              className=" 3/12 bg-white dark:bg-base p-5 m-3 boxShadow-2xl rounded-md"
            >
              <p className="w-full p-2 font-secondary text-base text-white60 dark:text-white20 mb-1 md:w-full">
>>>>>>> I fixed eslint issues
                {testimonial.text}
              </p>
              <div className="flex items-center ">
                <div className="w-12 h-12">
                  <img src={testimonial.image} alt="testimonial image" />
                </div>
                <div className=" ml-4">
                  <p className="text-primary font-semibold font-secondary text-xl ">
                    {testimonial.name}
                  </p>
                  <p className="font-secondary text-base, text-white60 ">
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
