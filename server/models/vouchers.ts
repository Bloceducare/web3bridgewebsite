import mongoose from "mongoose";

const Schema = mongoose.Schema;
const vouchersSchema = new Schema(
  {
    identifier: {
      type: String,
      required: true,
 
    },

    user: {
      type: String,
  
    
    },

    used:{
type:Boolean
    },
    
    valid: {
      type: Boolean,

    },

  },

  { timestamps: true }
);


const Vouchers =
  mongoose.models.vouchers || mongoose.model("vouchers", vouchersSchema, "vouchers");

export default Vouchers;
