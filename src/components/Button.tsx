import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-scroll";
type Props = {
  class: string;
  type: "background" | "transparent";
  content: string;
  clicked?: (e: any) => void;
  link?: string;
};

const Button = (props: Props) => {
  return (
    <Link to={props.link} spy={true} smooth={true}>
      <motion.button
        whileTap={{ scale: 0.5 }}
        transition={{ duration: 0.4 }}
        onClick={props.clicked}
        className={`${
          props.type === "background"
            ? "text-white bg-[#FA0101] border border-[#FA0101]"
            : " border "
        }
      ${props.class} rounded-sm text-sm outline-none `}
      >
        {props.content}
      </motion.button>
    </Link>
  );
};

export default Button;
