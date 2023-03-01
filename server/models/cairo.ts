import mongoose from "mongoose";
import  allUsersSChema  from "./users";

const Schema = mongoose.Schema;
const cairoUsersSchema = new Schema(
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


const cairoUsers =
  mongoose.models.cairoUsers || mongoose.model("cairoUsers", cairoUsersSchema, "cairoUsers");
export default cairoUsers;
