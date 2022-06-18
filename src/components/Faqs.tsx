import { faqData } from '../Data'
import React, { useEffect, useState } from 'react'
import Faq from 'react-faq-component'

const styles = {
  rowTitleColor: '#111111',
  rowContentColor: '#737373',
  rowTitleTextSize: '24px',
  rowContentTextSize: '16px',
  // arrowColor: "red",
  // bgColor: 'white',
}
const config = {
  animate: true,
  expandIcon: '+',
  collapseIcon: '-',
}
const Faqs = () => {
  return (
    <div className="flex flex-col items-center justify-center  py-6">
      <div className="text-3xl p-3 font-secondary text-center  font-semibold my-5 text-base90 md:text-5xl md:my-20 md:text">
        Frequently Asked Questions
      </div>
      <div className="w-11/12 md:w-2/4">
        <Faq data={faqData} styles={styles} config={config} />
      </div>
    </div>
  )
}

export default Faqs
