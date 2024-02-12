import reportError from "@server/services/report-error";
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
      
        return response
    } catch (error) {
        reportError(`error sending sms to ${data.recipients}\n environment:${process.env.NODE_ENV}\n ${error} `)
       
        console.log(error, "sms error")
        return error
    }
}

