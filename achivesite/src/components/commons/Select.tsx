import { IElementProps } from "types";

interface ISelectProps extends IElementProps {
    options:{label:string, value:string}[]
    name:string
    className?:string
    errors:any
    register:any
    label:string
    currentValue:string
    labelClassName?:string
    required?:boolean
    disabled?:boolean

}

const Select = ({options=[], name, className, label,register, errors, currentValue, labelClassName, required=true, disabled=false}:ISelectProps)=>{
    const err = errors[name]?.type === "required" || !!errors[name]?.message;

    return (
        <div className={disabled? "pointer-events-none" :""}>
            
            {err ? (
        <span className="absolute right-0 text-sm text-red-500 capitalize label-text-alt">
          {errors[name]?.message}
        </span>
      )
      : !!currentValue && (
        <span className="absolute right-0 text-sm text-gray-500 capitalize label-text-alt">
          All good
        </span>
      )
    }

            <label
    
    
    className={`block  dark:text-white20 relative   ${
      err ? "" : ""
    } dark:text-white20 ${labelClassName}`}
    htmlFor={name}
  >
    {label}
    {!!required &&  <span className="ml-1 text-red-500">*</span>}
    </label>
<div>
         
            <select 
            className={`bg-transparent border   text-sm rounded-md   block w-full p-2.5   dark:text-gray-400
            outline-none 
            dark:focus:text-gray-400
            
            ${
                err
                  ? "focus:ring-red-500 focus:border-red-500 ring-red-500 border-red-500"
                  :currentValue?.length > 0 ? "border-green-500" : ""          
              }
             ${className}`} name={name}  {...register(name)}>
                <option selected value="" disabled>Select an option</option>
               {options.map((option, index)=>(
                <option key ={index} value={option.value}>
                    {option.label}
                </option>
               ))}
            </select>
            </div>


        </div>
    )
}

export default Select