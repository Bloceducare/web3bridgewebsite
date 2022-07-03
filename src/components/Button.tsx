import React from 'react'
import { motion } from 'framer-motion'

type Props = {
  class: string
  type: 'background' | 'transparent'
  content: string
}

const Button = (props: Props) => {
  return (
    <motion.button
      whileTap={{ scale: 0.3 }}
      transition={{ duration: 0.4 }}
      className={`${
        props.type === 'background'
          ? 'text-white bg-[#FA0101] border border-[#FA0101]'
          : ' border '
      }
      ${props.class} rounded-sm text-sm `}
    >
      {props.content}
    </motion.button>
  )
}

export default Button
