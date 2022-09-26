import axios from "axios"
import {smsConfig} from "../config"

const config = {
    headers: { Authorization: `Bearer ${process.env.SMS_KEY}` }
};
export const sendSms = async (data: any={}) => {
    try {
        const smsData = {
            ...smsConfig,
           ...data,
        
        }
        const response = await axios.post(`https://app.multitexter.com/v2/app/sendsms`, smsData, config)
        // console.log(response.data, 'ssms daeadta')
        return response
    } catch (error) {
        console.log(error, "sms error")
        return error
    }
}

