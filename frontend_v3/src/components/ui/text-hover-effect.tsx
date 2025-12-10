"use client";
import React, { useRef, useEffect, useState } from "react";
import { motion } from "motion/react";
import { Londrina_Outline } from "next/font/google";
import { cn } from "@/lib/utils";

const londrina = Londrina_Outline({
  subsets: ["latin"],
  weight: ["400"]
});

export const TextHoverEffect = ({
  text,
  duration,
}: {
  text: string;
  duration?: number;
  automatic?: boolean;
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [cursor, setCursor] = useState({ x: 0, y: 0 });
  const [hovered, setHovered] = useState(false);
  const [maskPosition, setMaskPosition] = useState({ cx: "50%", cy: "50%" });

  useEffect(() => {
    if (svgRef.current && cursor.x !== null && cursor.y !== null) {
      const svgRect = svgRef.current.getBoundingClientRect();
      const cxPercentage = ((cursor.x - svgRect.left) / svgRect.width) * 100;
      const cyPercentage = ((cursor.y - svgRect.top) / svgRect.height) * 100;
      setMaskPosition({
        cx: `${cxPercentage}%`,
        cy: `${cyPercentage}%`,
      });
    }
  }, [cursor]);

  return (
    <svg
      ref={svgRef}
      width="100%"
      height="100%"
      viewBox="0 0 600 107"
      xmlns="http://www.w3.org/2000/svg"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onMouseMove={(e) => setCursor({ x: e.clientX, y: e.clientY })}
      className="select-none"
    >
      <defs>
        <linearGradient
          id="textGradient"
          x1="0%"
          y1="0%"
          x2="0%"
          y2="0%"
        >
          <stop offset="0%" stopColor="hsla(40, 100%, 98%, 0.15)" />
          <stop offset="25%" stopColor="hsla(40, 10%, 98%, 0.15)" />
          <stop offset="50%" stopColor="hsla(344, 10%, 73%, 0.15)" />
          <stop offset="75%" stopColor="hsla(344, 10%, 73%, 0.15)" />
          <stop offset="100%" stopColor="hsla(341, 100%, 92%, 0.15)" />
        </linearGradient>
        
        <linearGradient
          id="hoverGradient"
          x1="0%"
          y1="0%"
          x2="100%"
          y2="0%"
        >
          <stop offset="0%" stopColor="hsl(45, 93%, 67%)" />
          <stop offset="25%" stopColor="hsl(0, 84%, 70%)" />
          <stop offset="50%" stopColor="hsl(217, 91%, 70%)" />
          <stop offset="75%" stopColor="hsl(189, 94%, 63%)" />
          <stop offset="100%" stopColor="hsl(262, 83%, 68%)" />
        </linearGradient>

        <motion.radialGradient
          id="revealMask"
          gradientUnits="userSpaceOnUse"
          r="20%"
          initial={{ cx: "50%", cy: "50%" }}
          animate={maskPosition}
          transition={{ duration: duration ?? 0, ease: "easeOut" }}
        >
          <stop offset="0%" stopColor="white" />
          <stop offset="100%" stopColor="black" />
        </motion.radialGradient>
        <mask id="textMask">
          <rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#revealMask)"
          />
        </mask>
      </defs>
      
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        fill="url(#textGradient)"
        className={cn("text-[120px] ",londrina.className)}
      >
        {text}
      </text>
      
      {/* Animated stroke on load */}
      <motion.text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        strokeWidth="0.3"
        fill="transparent"
        stroke="url(#textGradient)"
        className={cn("text-[120px]", londrina.className)}
        initial={{ strokeDashoffset: 1000, strokeDasharray: 1000 }}
        animate={{
          strokeDashoffset: 0,
          strokeDasharray: 1000,
        }}
        transition={{
          duration: 4,
          ease: "easeInOut",
        }}
      >
        {text}
      </motion.text>
      
      
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        fill="url(#hoverGradient)"
        mask="url(#textMask)"
        className={cn("text-[120px]", londrina.className)}
        style={{ opacity: hovered ? 1 : 0 }}
      >
        {text}
      </text>
    </svg>
  );
};
