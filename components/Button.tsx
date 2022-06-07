type Props = {
  class: string;
  type: "background" | "transparent";
  content: string;
};

const Button = (props: Props) => {
  return (
    <button
      className={`${
        props.type === "background"
          ? "text-white bg-[#FA0101] border border-[#FA0101]"
          : "text-[#FA0101] border border-[#FA0101]"
      }
      ${props.class} rounded-sm text-sm `}
    >
      {props.content}
    </button>
  );
};

export default Button;
