import axios from "axios"
import {smsConfig} from "../config"

export const sendSms = async (data: any={}) => {
    try {
        const smsData = {
            ...smsConfig,
           ...data
        }
        const response = await axios.post(`https://app.multitexter.com/v2/app/sms`, smsData)

        // console.log(response.data, 'ssms daeadta')
        
        return response
    } catch (error) {
        console.log(error, "sms error")
        return error
    }
}

