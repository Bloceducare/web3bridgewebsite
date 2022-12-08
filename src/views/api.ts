
import axios from 'axios';

export const userRegistering = async(data)=>{
    const user = await axios.post('/api/cohort-users', data);
    return user;
}

export const specialClassRegistering = async(data)=>{
    const user = await axios.post('/api/special-class', data);
    return user;
}

export const initPayment = async(data)=>{
    const payment = await axios.post('/api/init-payment', data);
    return payment;
}

export const verifyPayment = async(data)=>{
    try{
        const payment = await axios.post('/api/verify-payment', data);
        return payment;
    }
    catch(e:any){
       throw e.response.data;
    }
}
