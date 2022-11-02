import vouchersDb from "../models/vouchers"


const useVoucher = async({identifier, email}) => {
 
    const voucher = await vouchersDb.findOne({identifier})
  
    if(!voucher) {
       
        throw  `${identifier} - invalid voucher`
    }

    if(voucher.used) {
   
       throw `${identifier} - voucher used`
    }

  try {
  
 const updated =  await vouchersDb.updateOne({identifier},{  $set: {valid: false, user:email, used:true}})


   
    return {
      status: true,
     code:201,
     message:'voucher applied successfully',
          data:updated,
       }

  }

  catch(e:any){
    return  {

            status:false,
            message:e
        }
  }

  };

  export default useVoucher