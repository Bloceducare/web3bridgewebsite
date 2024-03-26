'use client'
import React from 'react'

type CountDownNumTypes = {
    num: string,
    time: string,
    color: string
}

const gradientColors: { [key: string]: { gradient: string, text: string } } = {
    green: {
        gradient: 'from-green-700/30 to-transparent',
        text: 'text-green-700'
    },
    amber: {
        gradient: 'from-amber-600/30 to-transparent',
        text: 'text-amber-600'
    },
    purple: {
        gradient: 'from-purple-700/30 to-transparent',
        text: 'text-purple-700'
    },
    blue: {
        gradient: 'from-blue-900/40 to-transparent',
        text: 'text-blue-900'
    }
};

const CountDownNum = ({ num, time, color }: CountDownNumTypes) => {
    return (
        <div className={`lg:w-24 md:w-20 w-16 lg:h-24 md:h-20 h-16 flex flex-col gap-1 justify-center items-center bg-gradient-to-b rounded-lg ${gradientColors[color].gradient} ${gradientColors[color].text}`}>
            <h1 className={`tracking-widest font-semibold lg:text-5xl md:text-2xl text-2xl`}>{num}</h1>
            <p className={`font-light md:text-base text-sm`}>{time}</p>
        </div>

    )
}

export default CountDownNum;