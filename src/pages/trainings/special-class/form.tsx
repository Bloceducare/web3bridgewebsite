import SpecialClassView from "@views/specialized/components/form"

import { COHORT_REGISTRATION_OPENED } from "config/constant"

const  Form = ()=>{
    return (<>
    { COHORT_REGISTRATION_OPENED ? <div>
        {/* <div className="max-w-lg m-12 mx-auto bg-red-500 dark:text-white20 p-4 text-center text-xl font-semibold rounded-md">
            20 Registrations left to Close
         </div> */}
        <SpecialClassView />
    </div>:   <h1 className="font-bold text-center dark:text-white20 my-52">Registration has closed!!</h1>
   }
  
    </>)
}
export default Form