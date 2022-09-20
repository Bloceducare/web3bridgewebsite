import mongoose from "mongoose";
import  allUsersSChema  from "./users";

enum commitmentHours {
    yes="yes",
    no="no",
    maybe="maybe",
}
const Schema = mongoose.Schema;
const web2UsersSchema = new Schema(
  {
    ...allUsersSChema,
    twoHrMinDailyCommitment: {
        type: String,
        enum: commitmentHours,
        required: true,
    },
    inspirationForCoding:{
        type: String,
        required: true,
    },
    achievementFromProgram:{
        type: String,
        required: true,
    }
  },

  { timestamps: true }
);


const web2Users =
  mongoose.models.web2Users || mongoose.model("web2Users", web2UsersSchema, "web2Users");
export default web2Users;
