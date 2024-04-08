"use client"
import React, { useCallback, useEffect, useState } from "react";
import CountDownNum from "./CountDownNum";

interface TimeLeft {
    total: number;
    days: number;
    hours: number;
    minutes: number;
    seconds: number;
}

const CountDown = ({ targetDate }: { targetDate: string }) => {
    const [timeLeft, setTimeLeft] = useState<TimeLeft>({
        total: 0,
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0
    });

    const getTimeRemaining = useCallback((): TimeLeft => {
        const total = Date.parse(targetDate) - Date.parse(new Date().toISOString());
        const seconds = Math.floor((total / 1000) % 60);
        const minutes = Math.floor((total / 1000 / 60) % 60);
        const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
        const days = Math.floor(total / (1000 * 60 * 60 * 24));

        return {
            total,
            days,
            hours,
            minutes,
            seconds,
        };
    }, [targetDate]);

    useEffect(() => {
        const intervalId = setInterval(() => {
            setTimeLeft(getTimeRemaining());
        }, 1000);

        return () => clearInterval(intervalId);
    }, [getTimeRemaining]);

    function formatTime(value: number) {
        return value < 10 ? `0${value}` : `${value}`;
    }

    return (
        <main className="w-full  flex md:justify-start justify-center lg:gap-3 gap-1.5 lg:my-3 my-1.5 items-center">
            {timeLeft.total <= 0 ? (
                <>
                    <CountDownNum num={`00`} time={`Days`} color="green" />
                    <span className="font-medium text-gray-700 dark:text-gray-300 lg:text-5xl md:text-2xl text-xl">:</span>
                    <CountDownNum num={`00`} time={`Hours`} color="amber" />
                    <span className="font-medium text-gray-700 dark:text-gray-300 lg:text-5xl md:text-2xl text-xl">:</span>
                    <CountDownNum num={`00`} time={`Mins`} color="purple" />
                    <span className="font-medium text-gray-700 dark:text-gray-300 lg:text-5xl md:text-2xl text-xl">:</span>
                    <CountDownNum num={`00`} time={`Secs`} color="blue" />
                </>
            ) : (
                <>
                    <CountDownNum
                        num={`${formatTime(timeLeft.days)}`}
                        time={`Days`}
                        color="green"
                    />
                    <span className="font-medium text-gray-700 dark:text-gray-300 lg:text-5xl md:text-2xl text-xl">:</span>
                    <CountDownNum
                        num={`${formatTime(timeLeft.hours)}`}
                        time={`Hours`}
                        color="amber"
                    />
                    <span className="font-medium text-gray-700 dark:text-gray-300 lg:text-5xl md:text-2xl text-xl">:</span>
                    <CountDownNum
                        num={`${formatTime(timeLeft.minutes)}`}
                        time={`Mins`}
                        color="purple"
                    />
                    <span className="font-medium text-gray-700 dark:text-gray-300 lg:text-5xl md:text-2xl text-xl">:</span>
                    <CountDownNum
                        num={`${formatTime(timeLeft.seconds)}`}
                        time={`Secs`}
                        color="blue"
                    />
                </>
            )}
        </main>
    );
};

export default CountDown;
