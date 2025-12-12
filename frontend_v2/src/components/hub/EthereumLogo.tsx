"use client";

import React from "react";
import { motion } from "framer-motion";

interface EthereumLogoProps {
  className?: string;
  size?: number;
  animated?: boolean;
}

export default function EthereumLogo({ className = "", size = 40, animated = true }: EthereumLogoProps) {
  const logo = (
    <svg
      width={size}
      height={size}
      viewBox="0 0 784.37 1277.39"
      className={className}
      xmlns="http://www.w3.org/2000/svg"
    >
      <polygon
        points="392.07,0 383.5,29.11 383.5,873.74 392.07,882.29 784.13,650.54"
        fill="#8C92AC"
      />
      <polygon
        points="392.07,0 -0,650.54 392.07,882.29 392.07,472.33"
        fill="#62688F"
      />
      <polygon
        points="392.07,956.52 387.24,962.41 387.24,1263.28 392.07,1277.38 784.37,724.89"
        fill="#454A75"
      />
      <polygon
        points="392.07,1277.38 392.07,956.52 -0,724.89"
        fill="#8C92AC"
      />
      <polygon
        points="392.07,882.29 784.13,650.54 392.07,472.33"
        fill="#62688F"
      />
      <polygon
        points="0,650.54 392.07,882.29 392.07,472.33"
        fill="#454A75"
      />
    </svg>
  );

  if (!animated) {
    return logo;
  }

  return (
    <motion.div
      animate={{
        rotate: [0, 360],
        scale: [1, 1.1, 1],
      }}
      transition={{
        rotate: {
          duration: 20,
          repeat: Infinity,
          ease: "linear",
        },
        scale: {
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
        },
      }}
      className="inline-block"
    >
      {logo}
    </motion.div>
  );
}

