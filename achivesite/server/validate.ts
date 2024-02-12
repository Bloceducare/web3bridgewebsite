
const validate = (schema) => async (req, res, next) => {
    try {
      await schema.validate({
        ...(req.body),
         ...(req.query),
        ...(req.params),
      }, {
        abortEarly: false,
      });
      return next();
    } catch (err:any) {
      return res.status(500).json({ 
        type: err.name, 
        errors: err.errors,
        message: err.message 
      });
    }
  };


 export  const validateCoupon = (schema) => async (req, res, next) => {
    try {
      await schema.validate({
       
         ...(req.query),
      
      }, {
        abortEarly: false,
      });
      return next();
    } catch (err:any) {
      return res.status(500).json({ 
        type: err.name, 
        errors: err.errors,
        message: err.message 
      });
    }
  };

  export default validate;