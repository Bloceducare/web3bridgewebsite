import CohortRegistration from "@views/registration";
import { COHORT_REGISTRATION_OPENED } from "config/constant"


const  Web3Registration = ()=>{
    return (<>
      { COHORT_REGISTRATION_OPENED ?    <CohortRegistration />:   <h1 className="font-bold text-center dark:text-white20 my-52">Registration has closed!!</h1>
   }
   
    </>)
}

export default Web3Registration