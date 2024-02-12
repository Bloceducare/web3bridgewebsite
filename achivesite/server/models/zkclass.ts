import mongoose from "mongoose";
import  allUsersSChema  from "./users";

const Schema = mongoose.Schema;
const zkclassUsersSchema = new Schema(
  {
    ...allUsersSChema,
    prevCohort:{
        type:String
    },    
     githubUsername:{
            type:String
      },
      alumni:{
        type:String
      } ,
      walletAddress: {
        type: String,   
      },
 
  },

  { timestamps: true }
);


const zkclassUsers =
  mongoose.models.zkclassUsers || mongoose.model("zkclassUsers", zkclassUsersSchema, "zkclassUsers");
export default zkclassUsers;
