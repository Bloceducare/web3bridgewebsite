import mongoose from "mongoose";
import  allUsersSChema  from "./users";


const Schema = mongoose.Schema;
const specialClassSchema = new Schema(
  {
    ...allUsersSChema,
    AreaOfInterest: {
        type: String,
        required: true,
    }, 
    trainingTime: {
        type: String,        
    }, 
  
  },

  { timestamps: true }
);


const specialClass =
  mongoose.models.specialClass || mongoose.model("specialClass", specialClassSchema, "specialClass");
export default specialClass;
