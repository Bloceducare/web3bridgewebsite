import React from 'react'
import type { NextPage } from 'next'
import HeroSection from '../components/HeroSection'
import Mission from '../components/Mission'
import Partners from '../components/Partners'
const Home: NextPage = () => {
  return (
    <div className="">
      <HeroSection />
      <Mission />
      <Partners />
    </div>
  )
}

export default Home
