'use client'
import { motion } from "framer-motion";


const SVGLine = (): JSX.Element => {
    return (
        <div className="w-full h-full relative -mt-[200px]">
            <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" id="eADtBMPrzR31" viewBox="0 0 300 300" shapeRendering="geometricPrecision" textRendering="geometricPrecision">
                <g>
                    <path d="M34.855178,78.569911h233.788498l9.174841,22.767196-.000001,18.689486-9.17484,20.72834h-233.788498L21.942441,165.22117v18.349679l12.912737,20.72834h233.788498" transform="translate(.000005 0.000002)" fill="none" stroke="#f9d2d2" strokeWidth={0.8}

                    />
                </g>
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" id="eADtBMPrzR31" viewBox="0 0 300 300" shapeRendering="geometricPrecision" className="absolute top-0 left-0 " textRendering="geometricPrecision">
                <g>
                    <motion.path d="M34.855178,78.569911h233.788498l9.174841,22.767196-.000001,18.689486-9.17484,20.72834h-233.788498L21.942441,165.22117v18.349679l12.912737,20.72834h233.788498" transform="translate(.000005 0.000002)" fill="none" stroke="#FA0101" strokeWidth={0.8}
                        initial={{ pathLength: 0 }}
                        animate={{ pathLength: 1 }}
                        transition={{
                            repeat: Infinity,
                            repeatType: "mirror",
                            ease: "easeInOut",
                            duration: 8,
                        }}
                    />
                </g></svg>
        </div>
    )
}

export default SVGLine