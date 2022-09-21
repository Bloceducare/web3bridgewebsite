import Button from "@components/commons/Button"
import { useRouter } from 'next/router'
const ConfirmPayment =()=>{
    const {push} = useRouter()
    return (<>
    <div className="text-xl font-semibold flex  items-center justify-center flex-col p-3 capitalize h-[calc(100vh-20rem)]">
   
    <div className="flex flex-col items-center justify-center dark:text-white20 ">
        <div className="px-5 mt-2 text-sm font-semibold">
            Thank you for trusting us, we've already received your payment
        </div>

        <Button onClick={()=>push("/")} className="mt-4">Go Back Home</Button>

          
        </div>
        </div>
    
    </>)
}

export default ConfirmPayment