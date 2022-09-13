import React, { useState } from 'react'
import { toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

toast.configure()
const Newsletter = () => {
  const [input, setInput] = useState('')

  const notify = () =>
    toast.success('you have successfully registered for our news letter!', {
      position: toast.POSITION.TOP_CENTER,
    })

  const inputHandler = (e) => {
    setInput(e.target.value)
  }
  const submitHandler = (e) => {
    e.preventDefault()
    if (input) {
      console.log(input)
      notify()
      setInput('')
    }
  }
  return (
    <div className="flex flex-col items-center justify-center bg-base py-6 mt-20">
      <div className="flex flex-col items-center justify-center">
        <h1 className=" text-white mt-7 mb-6 text-2xl font-bold text-center md:mt-0 md:text-5xl ">
          Subscribe to our Newsletter
        </h1>
        <p className=" w-11/12  m-2/5 mb-20 text-xl md:text-center text-white10 md:w-4/5 ">
          Get occasional news and update from us about the latest trends,
          technology in the web 3 world, we promise not to spam you.
        </p>
        <form
          onSubmit={submitHandler}
          className="w-full md:w-full flex justify-center px-2 "
        >
          <div className=" w-full  md:w-2/5 px-4">
            <input
              onChange={inputHandler}
              value={input}
              type="email"
              className="pl-2 py-3 w-11/12  border-2 bg-base90 text-white10"
              placeholder="Enter your email address here"
            />
          </div>
          <div className="">
            <button
              type="submit"
              className="bg-white  text-base font-base w-28 py-3 border-2 md:w-48"
            >
              Subscribe
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Newsletter
