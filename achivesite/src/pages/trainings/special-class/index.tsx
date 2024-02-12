import SpecialClassView from "@views/specialized"
import { COHORT_REGISTRATION_OPENED } from "config/constant"

const  Web2Registration = ()=>{
    return (<>
    { COHORT_REGISTRATION_OPENED ?   <SpecialClassView />:   <h1 className="font-bold text-center dark:text-white20 my-52">Registration has closed!!</h1>
   }
  
    </>)
}
export default Web2Registration