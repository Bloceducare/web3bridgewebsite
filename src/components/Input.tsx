type Props = {
  type: string;
  placeholder: string;
  
};

const Input = (props: Props) => {
  return (
    <input
      type={props.type}
      placeholder={props.placeholder}
      className="my-4 px-6 py-2 text-white60 rounded-md outline-none w-full border bg-[#0000] border-white10"
    />
  );
};

export default Input;
