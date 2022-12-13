import { Gender,Tracks,PaymentMethod,PaymentStatus } from "enums"

const allUserSchema =  {
    name: {
      type: String,
      required: true,
      trim: true
      
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
      lowercase: true,
    },

    twitterHandle: {
      type: String,
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

    walletAddress: {
      type: String,   
    },

    phone: {
      type: String,
      required: true,
      
    },
    paymentStatus:{
      type: String,
      enum:PaymentStatus,
    },
    paymentMethod:{
      type: String,
      enum:PaymentMethod,
      required:true
    },
    acceptanceSent:{
      type:Boolean,
      default:false
    }
  }



export default allUserSchema