import { IElementProps } from "types";

interface ITextAreaProps extends IElementProps {
  placeholder?: string;
  name: string;
  required: boolean;
  label: string;
  errors: any;
  disabled?: boolean;
  className?: string;
  register: (string)=>any;
  currentValue?: string;
}

const TextArea = ({
  placeholder = "",
  className = "",
  name,
  required=false,
  label,
  errors,
  disabled = false,
  register,
  currentValue="",
}: ITextAreaProps) => {
  const err =
    errors[name]?.type === "required" || !!errors[name]?.message;

  return (
    <div className="relative">
      
      {err ? (
        <span className="absolute right-0 text-sm text-red-500 capitalize label-text-alt">
          {errors[name]?.message}
        </span>
      )
      : currentValue && (
        <span className="absolute right-0 text-sm text-gray-500 capitalize label-text-alt">
          All good
        </span>
      )
    }
      <label
    
        className={`dark:text-white20 relative  ${
          err ? "" : ""
        }`}
        htmlFor={name}
      >
        {label}
        </label>
        <textarea
          disabled={disabled}
          placeholder={placeholder}
          name={name}
          id={name}
          required={required}
          rows={3}
          className={`lowercase my-4 mt-1 px-6 py-2 text-white60 rounded-md outline-none w-full border bg-[#0000] border-white10   ${
            err
              ? "focus:ring-red-500 focus:border-red-500 ring-red-500 border-red-500"
              :currentValue.length > 0 ? "border-green-500" : ""          
          } 
          
          ${className}`}
          {      
             ...register(name)
                
        }
        />        
   
    </div>
  );
};

export default TextArea;