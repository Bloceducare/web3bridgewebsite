import { useEffect, useState } from "react"


const initState = {
        currency:{
            code:""
        }
    }
const useCountry = ()=>{
    const [country, setCountry] = useState(initState)

    useEffect(()=>{

        async function getCountry(){
            try {

                const {data={} } = await fetch("/api/country").then(info=>info.json())
            
               const temp= {
                ...data,
                currency:{
                    ...data?.currency,
                    code:"USD"
                }
               }
           

                setCountry(data)
                
            } catch (error) {
                setCountry(initState)                
            }
        }

        getCountry()

    },[])


    return country


}
export default useCountry