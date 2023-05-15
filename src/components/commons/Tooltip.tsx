import { useState } from "react";

const Tooltip = ({ text, children }) => {
  const [isTooltipVisible, setTooltipVisible] = useState(false);

  const handleMouseEnter = () => {
    setTooltipVisible(true);
  };

  const handleMouseLeave = () => {
    setTooltipVisible(false);
  };

  return (
    <div className="relative inline-block">
      <div
        className="relative z-10"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {children}
        <svg
          className="h-3 w-3 inline-flex ml-2"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="16" x2="12" y2="12" />
          <line x1="12" y1="8" x2="12" y2="8" />
        </svg>
      </div>
      {isTooltipVisible && (
        <div className="absolute z-20 bottom-full left-1/2 transform -translate-x-1/2">
          <div className="px-2 py-1 text-xs font-semibold text-white bg-gray-900 rounded-lg">
            {text}
          </div>
          <svg
            className="absolute w-3 h-3 text-gray-900 fill-current top-full left-1/2 transform -translate-x-1/2 -mt-1"
            x="0px"
            y="0px"
            viewBox="0 0 255 255"
            xmlSpace="preserve"
          >
            <polygon className="fill-current" points="0,0 127.5,127.5 255,0" />
          </svg>
        </div>
      )}
    </div>
  );
};

export default Tooltip;
