import axios from 'axios'

async function reportError(error){ 
  
    try{
        await axios.post(`${process.env.ERROR_REPORTING}${encodeURI(error)}`)
 
    }

    catch(e){
        console.log("e", e)
    }

}

export default reportError