import { useState, useEffect } from "react";
import { motion } from "framer-motion";

const Countdown = ({ timestamp }) => {
  const [days, setDays] = useState(0);
  const [hours, setHours] = useState(0);
  const [minutes, setMinutes] = useState(0);
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date().getTime();
      const distance = timestamp - now;

      setDays(Math.floor(distance / (1000 * 60 * 60 * 24)));
      setHours(
        Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      );
      setMinutes(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)));
      setSeconds(Math.floor((distance % (1000 * 60)) / 1000));
    }, 1000);

    return () => clearInterval(interval);
  }, [timestamp]);

  return (
    <div className="flex items-center justify-center  dark:text-black text-white  ">
      <div className="text-6xl font-bold flex items-center">
        <motion.div className="text-center" animate={{ scale: [1, 1.1, 1] }}>
          <div className="text-3xl">{days}</div>
          <div className="text-xs">Days</div>
        </motion.div>
        <div className="mx-2 text-2xl">:</div>
        <motion.div className="text-center" animate={{ scale: [1, 1.1, 1] }}>
          <div className="text-3xl">{hours}</div>
          <div className="text-xs">Hours</div>
        </motion.div>
        <div className="mx-2 text-2xl">:</div>
        <motion.div className="text-center" animate={{ scale: [1, 1.1, 1] }}>
          <div className="text-3xl">{minutes}</div>
          <div className="text-xs">Minutes</div>
        </motion.div>
        <div className="mx-2 text-2xl">:</div>
        <motion.div className="text-center" animate={{ scale: [1, 1.1, 1] }}>
          <div className="text-3xl">{seconds}</div>
          <div className="text-xs">Seconds</div>
        </motion.div>
      </div>
    </div>
  );
};

export default Countdown;
