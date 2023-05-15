import { Schema, models, model } from "mongoose";
import allUsersSChema from "./users";

enum commitmentHours {
  yes = "yes",
  no = "no",
  maybe = "maybe",
}

enum EClassCat {
  basic = "basic",
  advanced = "advanced",
}

const web2UsersSchema = new Schema(
  {
    ...allUsersSChema,
    twoHrMinDailyCommitment: {
      type: String,
      enum: commitmentHours,
      required: true,
    },
    inspirationForCoding: {
      type: String,
      required: true,
    },
    achievementFromProgram: {
      type: String,
      required: true,
    },
    classCat: {
      type: String,
      enum: EClassCat,
      required: true,
    },
  },

  { timestamps: true }
);

const web2Users =
  models.web2Users || model("web2Users", web2UsersSchema, "web2Users");
export default web2Users;
