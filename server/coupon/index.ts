import vouchersDb from "../models/coupons"


const useCoupon = async({identifier, email}) => {

 
    const coupon = await vouchersDb.findOne({identifier})
  
    if(!coupon) {
       
        throw  {
            code:423,
            status:false,
            message:'invalid coupon'
        }
    }

    if(coupon.used) {
        
       throw  {
        code:423,
            status:false,
            message:'coupon used'
        }
    }

  try {
  
 const updated =  await vouchersDb.updateOne({identifier},{  $set: {valid: false, user:email, used:true}})


   
    return {
      status: true,
     code:201,
     message:'coupon applied successfully',
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

  export default useCoupon;