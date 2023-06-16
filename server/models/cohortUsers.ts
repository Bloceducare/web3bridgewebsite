import { Gender, PaymentMethod, PaymentStatus, Tracks } from "enums";
import mongoose from "mongoose";
import allUserSchema from "./users";

const Schema = mongoose.Schema;
const cohortUsersSchema = new Schema(
  {
    ...allUserSchema,
    name: {
      type: String,
      required: true,
      
    },
    country:{
      type: String,
    },
    city:{
      type: String,
    },
    email: {
      type: String,
      required: true,
      trim: true,
      unique: true,
    },

    twitterHandle: {
      type: String,
      default:"joe",
    },
    gender:{
      type: String,
      required: true,
      enum:Gender,
    },
    currentTrack:{
      type: String,
      enum:Tracks,
      required: true
    },
    githubUsername: {
      type: String,
    },
    progLang: {
      type: [String],

    },
    paymentReference: {
      type: String,
    },
    walletAddress: {
      type: String,
      required:function(){ // @ts-ignore
        return this.currentTrack === Tracks.web3
      }
    },
    phone: {
      type: String,
      required: true,
      
    },
    
    nextOfKin: {
      type: String,

    },
    nextOfKinPhone: {
      type: String,
      required:function(){ // @ts-ignore
        return this.nextOfKin !== undefined
      }
    },
    nextOfKinAddress: {
      type: String,
      required:function(){ // @ts-ignore
        return this.nextOfKin
      }
    },
    nextOfKinRelationship: {
      type: String,
      required:function(){ // @ts-ignore
        return this.nextOfKin
      }
    },
    profilePicture:{
      type: String,
    },
    socials: {
      type: [String],
 

    },

    paymentStatus:{
      type: String,
      enum:PaymentStatus,
    }
  },

  { timestamps: true }
);


const CohortUsers =
  mongoose.models.web3Users || mongoose.model("web3Users", cohortUsersSchema, "web3Users");

export default CohortUsers;
