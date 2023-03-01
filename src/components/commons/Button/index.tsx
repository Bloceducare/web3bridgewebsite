type IProps ={
    children: React.ReactNode
    className?: string
    disabled?: boolean
    onClick?: (e: any) => void
    type?: "button" | "submit" | "reset" 
}


const Button = ({className, disabled, children, onClick, type='button'}:IProps) => {
    return (
        <>
            <button
            type={type}
            onClick={onClick}
            className={`bg-[#FA0101] text-white text-sm px-6 py-2 rounded-md ${disabled ? "cursor-not-allowed bg-red-400":""} ${className}`}

             disabled={disabled}
             >
                {children}
             </button>
        </>
    )
}

export default Button