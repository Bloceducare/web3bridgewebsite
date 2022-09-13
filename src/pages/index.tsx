import type { NextPage } from 'next'
import React from 'react'
import Mission from '../components/Mission'
import Partners from '../components/Partners'
import Career from '../components/Career'
import Products from '../components/Products'
import Community from '../components/Community'
import Newsletter from '../components/Newsletter'
import Testimonial from '../components/Testimonial'
import Faqs from '../components/Faqs'
import dynamic from 'next/dynamic'

const DynamicComponentWithNoSSR = dynamic(
  () => import('../components/HeroSection'),
  { ssr: false },
)

const Home: NextPage = () => {
  return (
    <div className="">
      <DynamicComponentWithNoSSR />
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
