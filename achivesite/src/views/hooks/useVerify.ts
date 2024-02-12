import { useState, useEffect, useCallback } from "react"
import { verifyPayment } from "@views/api"

interface IVerifyPayment {
    status: boolean;
    message: string;
    error?:any
}
const defaultState = {
    status: true,
    message:"",
    error: null,
}
const useVerify = ({reference, email, currentTrack}) => {
    const [isVerified, setIsVerified] = useState<IVerifyPayment>(defaultState)
    const [isVerifying, setIsVerifying] = useState(true)
    const [error, setError] = useState<IVerifyPayment>()

    const verify = async () => {
        setIsVerifying(true)
        try{

            const {data} = await verifyPayment({reference, email, currentTrack});
           
            setIsVerified(data)
        }
        catch(e:any){  
            setError(e)
            
        }
        finally{
            setIsVerifying(false)
        }
    }

    const verifyCallback = useCallback(async () => {
            try{await verify()}
            catch(e:any){console.log(e, 'callabck error')}
    }, [reference, email])
    useEffect(() => {
        if(!reference || !email) return;
        
        verifyCallback()
    }, [reference, email])
    return { isVerified, isVerifying, error, verify }
}

export default useVerify