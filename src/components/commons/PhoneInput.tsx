import PhoneInput2 from 'react-phone-input-2'


const PhoneInput = ({field={}, name, value, handleChange, errors, currentValue="", disabled=false, required=true}) => {
    const err = errors?.[name]?.type === "required" || !!errors?.[name]?.message;

    return (
        <div className='relative'>
            <div>
              {err ? (
        <span className="absolute right-0 text-sm text-red-500 capitalize label-text-alt">
          {errors?.[name]?.message}
        </span>
      )
      : currentValue && (
        <span className="absolute right-0 text-sm text-gray-500 capitalize label-text-alt">
          All good
        </span>
      )
    }
    </div>
    <div className='dark:text-white20'>Phone
    {!!required &&  <span className="ml-1 text-red-500">*</span>}
    </div>
             <PhoneInput2  
             containerClass={`my-4 mt-1 pr-6 text-white60 rounded-md outline-none w-full border bg-transparent border-white10  ${
                err
                  ? "focus:ring-red-500 focus:border-red-500 ring-red-500 border-red-500"
                  :currentValue.length > 0 ? "border-green-500" : ""          
              } 
              `
            }
     
            dropdownClass='dark:bg-gray-800 dark:text-white20 dark:drop-down-custom'
            // dropdownStyle={{width: '100%'}}
            enableSearch
            searchClass='dark:bg-gray-800 dark:text-white20 w-full'
            buttonStyle={{
                borderLeft:'none',
                borderTop:'none',
                borderBottom:'none',
                backgroundColor: 'transparent',
                borderRight: `1px solid ${err ? 'red' :currentValue.length > 0 ? "border-green-500" : "#ccc"}`,
            }}
                value={value}  // @ts-ignore
                name={name} 
                disabled={disabled}
                country={'ng'} // @ts-ignore
                onChange={handleChange}
                placeholder="813 019 2777" 
                inputClass="border border-red-60"
                {...{...field, required:true, name:"phone"}}
                inputStyle={{
                  backgroundColor:"transparent",
                  width: '105%', height: '40px', border: 'none', 
                ...err && {borderColor: 'red'}
                }}
                />
        </div>
    )
}

export default PhoneInput