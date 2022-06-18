import React from 'react'
import type { NextPage } from 'next'
import HeroSection from '../components/HeroSection'
import Mission from '../components/Mission'
import Partners from '../components/Partners'
import Career from '../components/Career'
import Community from '../components/Community'
import Newsletter from '../components/Newsletter'
import Testimonial from '../components/Testimonial'
import Faqs from '../components/Faqs'
const Home: NextPage = () => {
  return (
    <div className="">
      <HeroSection />
      <Mission />
      <Partners />
      <Career />
      <Community />
      <Newsletter />
      <Testimonial />
      <Faqs />
    </div>
  )
}

export default Home
