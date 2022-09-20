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

const TimeToRedirect=12

const MessageBlock = ({message, children, count=TimeToRedirect, status}:IMessageProps) => {
    const {push} = useRouter() 
    return (<div className="text-xl font-semibold flex  items-center justify-center flex-col p-3 capitalize h-[calc(100vh-20rem)]">
    {children ? <>
    {children}
   {status &&
   <>
    <div className="flex flex-col items-center justify-center dark:text-white20 ">
        <div className="mt-2 text-sm font-semibold ">Redirecting To Home in {count > 0 ? count : 0} seconds</div>
            <Button onClick={()=>push("/")} className="mt-4">Go Back Home</Button>
        </div>
    </> 
    }
 
    </>: message}
</div>)
}

const VerifyPaymentView = () => {
    const {query:{email, reference, currentTrack}={}, push} = useRouter()
    const {
        isVerified, 
        isVerifying,
        error,
        verify
    } = useVerify({email, reference, currentTrack})
    
    const status = isVerified?.status
    const [count, setCount] = useState(TimeToRedirect)
    useEffect(() => {
            const timer = setInterval(() =>setCount(count => count <=0 ? 0 :count - 1), 1000)
            return () => clearInterval(timer)              
    }, [status])
  
    const  _status =()=>{
        if(isVerifying){
            return <MessageBlock  message="Please wait..." > 
             <div className="flex p-5 space-x-3 rounded-full loader">
  <div className="w-5 h-5 bg-gray-800 rounded-full dark:bg-white20 animate-bounce" />
  <div className="w-5 h-5 bg-gray-800 rounded-full dark:bg-white20 animate-bounce" />
  <div className="w-5 h-5 bg-gray-800 rounded-full dark:bg-white20 animate-bounce" />
</div>


            </MessageBlock>
        }
      
        if(error){
            return <>
           <MessageBlock       
           status={isVerified.status}
           count={count}
           > 
           <span className="dark:text-white20">
                {error?.message} 
            
           </span>
                { (isVerifying && error?.message) && <Button className="mt-4 dark:text-wite20" onClick={verify}>Try Again</Button>}
      
            </MessageBlock>
            </>
        }
        return <MessageBlock 
  
        count={count} 
        status={isVerified.status} 
        >
           <span className="dark:text-white20">
            
               {isVerified?.message}
           </span>
            </MessageBlock>
    }

    // console.log(status, count)
    if(status && count <= 0){
        push("/")
      }

    return (<>
        {_status()}
    </>)
}


export default VerifyPaymentView