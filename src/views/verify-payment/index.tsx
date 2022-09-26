import { useState, useEffect } from "react"
import {useRouter} from "next/router"
import useVerify from "../hooks/useVerify"
import Button from "@components/commons/Button"

interface IMessageProps {
    message?: string
    status?: boolean
    count?: number
    children?: React.ReactNode,
    
}

const TimeToRedirect=25

const MessageBlock = ({ children, count=TimeToRedirect, status}:IMessageProps) => {
    const {push} = useRouter() 
    return (<div className="text-xl font-semibold flex  items-center justify-center flex-col p-3 capitalize h-[calc(100vh-20rem)]">

   {children}
    <div className="flex flex-col items-center justify-center dark:text-white20 ">
        <div className="mt-2 text-xs font-semibold ">Redirecting To Home in {count > 0 ? count : 0} seconds</div>
            <Button onClick={()=>push("/")} className="mt-4">Go Back Home</Button>
        </div>
</div>)
}

const VerifyPaymentView = () => {
    const {push} = useRouter() 
    const [count, setCount] = useState(TimeToRedirect)
    useEffect(() => {
            const timer = setInterval(() =>setCount(count => count <=0 ? 0 :count - 1), 1000)
            return () => clearInterval(timer)              
    }, [])
  
    const  _status =()=>{
        return <MessageBlock 
        count={count}  
        >
           <div className="max-w-lg text-lg text-center dark:text-white20 ">
           Your Registration was successful 🎉🎉🎉
           <br /> 
           <p className="mt-2 text-sm ">  We're currently verifying your payment, You will receive an sms and email shortly for further instructions, Happy Learning! </p>
           </div>
            </MessageBlock>
    }

    if( count <= 0){
        push("/")
      }


    return (<>
        {_status()}
    </>)
}


export default VerifyPaymentView