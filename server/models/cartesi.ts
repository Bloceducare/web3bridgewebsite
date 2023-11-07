import mongoose from "mongoose";
import  allUsersSChema  from "./users";

const Schema = mongoose.Schema;
const cartesiUsersSchema = new Schema(
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


const cartesiUsers =
  mongoose.models.cartesiUsers || mongoose.model("cartesiUsers", cartesiUsersSchema, "cartesiUsers");
export default cartesiUsers;
