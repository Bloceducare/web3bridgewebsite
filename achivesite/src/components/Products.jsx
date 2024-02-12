import React from 'react'
import Button from '../components/Button'

const Products = () => {
  return (
    <div className="w-full my-20 flex flex-col items-center justify-center ">
      <div className="w-11/12 md:w-1/2">
        <p className="font-secondary mb-6 font-semibold text-base90 dark:text-white10 md:text-4xl text-center">
          Take an inside look to our Products
        </p>
        <p className="font-primary text-xl md:text-center text-white60 dark:text-white20 mb-24">
          Adipiscing magna viverra magna malesuada aliquam eu netus. Amet nunc
          in vitae, arcu nullam nunc blandit. Quam sit neque eget amet. Mi diam
          orci amet.
        </p>
      </div>
      <div className="w-11/12 md:w-9/12 lg:w-9/12 flex items-center justify-between flex-col  md:flex-row">
        <div className="w-11/12 md:w-6/12 mt-10 ">
          <div className="md:w-10/12 lg:w-8/12">
            <p className="font-secondary font-semibold text-xl md:text-3xl text-base90 dark:text-white10">
              Web 3 bridge built dapps
            </p>
            <p className=" mb-14 text text-white60 dark:text-white20 ">
              Tellus leo, quis ultricies justo, id libero. Vitae, sed dictumst
              sit ullamcorper senectus auctor. Euismod eros viverra lacus turpis
              condimentum pharetra, habitasse venenatis.
            </p>
            <Button
              content="Scale dapp"
              class="mb-14 text-base dark:text-white dark:bg-[#FA0101] dark:border-[#FA0101] px-14 py-2"
            />
          </div>
        </div>
        <div className=" w-11/12 md:w-6/12">
          <img src="./product.png" alt="product" />
        </div>
      </div>
    </div>
  )
}

export default Products
