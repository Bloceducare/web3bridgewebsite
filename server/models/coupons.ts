import mongoose from "mongoose";

const Schema = mongoose.Schema;
const couponsSchema = new Schema(
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


const Coupons =
  mongoose.models.coupons || mongoose.model("coupons", couponsSchema, "coupons");

export default Coupons;
