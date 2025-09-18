import { useEffect, useState } from "react";

interface ScrollTriggerArgs {
  onEnter?: () => void;
  onExit?: () => void;
}

export const useScrollTrigger = ({ onEnter, onExit }: ScrollTriggerArgs) => {
  const [isTriggered, setIsTriggered] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;

      const triggerThreshold = 50;
      const shouldTrigger = scrollY > triggerThreshold;

      if (shouldTrigger && !isTriggered) {
        setIsTriggered(true);
        if (onEnter) {
          onEnter();
        }
      } else if (!shouldTrigger && isTriggered) {
        setIsTriggered(false);
        if (onExit) {
          onExit();
        }
      }
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [isTriggered, onEnter, onExit]);

  return isTriggered;
};
