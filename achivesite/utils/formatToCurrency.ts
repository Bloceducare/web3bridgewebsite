export default function formatToCurrency(amount:number){
    return (amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'); 
}


export const showTime = ()=>{
    
}