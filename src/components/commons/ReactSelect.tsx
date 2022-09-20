import Select from 'react-select'
// import AsyncSelect from 'react-select/async';
// import CreatableSelect from 'react-select/creatable';

const customStyles ={
  control: (provided, state) => ({
    ...provided,
    '&:hover': { borderColor: 'gray' }, // border style on hover
    border: '1px solid #ccc', // default border color
    boxShadow: 'none', // no box-shadow
    padding:"0.25rem 0"
    }),
  menu: (provided, state) => ({
    ...provided,
    border: "none",
    boxShadow: "none",
    // backgroundColor: " #8798aafb",
    zIndex: 99,
    
  }),
  option: (provided, state) => ({
    ...provided,
     backgroundColor: state.isFocused && "#cbd5e058",
     cursor:"pointer",
  })
}
type IOptions = {
    value: string;
    label: string;
}
interface IProps { 
    field: any;
    name: string;
    errors?: any;
    currentValue?: string;
    handleChange?: any;
    value?: string;
    options:IOptions[]
    defaults?:IOptions[]
    isMulti?: boolean;
    [key: string]: any;
    placeholder?:string;
    disabled?:boolean;
    label:string;
    isLoading?:boolean;
    
 }
const ReactSelect=({errors, field={}, name, defaults=[], options=[], isMulti=false, placeholder, disabled, isLoading, value, label}:IProps)=>{

    const err =
    errors?.[name]?.type === "required" || !!errors?.[name]?.message;

    return (
        <div className='relative '>
            <label
    
    className={`  relative  ${
      err ? "" : ""
    } dark:text-white20`}
    htmlFor={name}
  >
    {label}
</label>
              <div>
              {err ? (
        <span className="absolute right-0 text-sm text-red-500 capitalize label-text-alt">
          {errors?.[name]?.message}
        </span>
      )
      : ''

    }
    </div>
    
          <Select
          styles={customStyles}
          defaultValue={defaults}
          isMulti={isMulti}
          name={name}
          isLoading = {isLoading}
          options={options}
          className="dark:cs-select basic-multi-select custom-select-react dark:react-select__menu"
          classNamePrefix="react-select"
          placeholder={placeholder}
          isDisabled={disabled}
          value={value}
          {...field} 
      />
      </div>
    )
}

export default ReactSelect