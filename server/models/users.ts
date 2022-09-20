import { Gender,Tracks,PaymentMethod,PaymentStatus } from "enums"

const allUserSchema =  {
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
     required:true
    },

    phone: {
      type: String,
      required: true,
      
    },
    
    // nextOfKin: {
    //   type: String,
    // },
    // nextOfKinPhone: {
    //   type: String,
    //   required:function(){ // @ts-ignore
    //     return this.nextOfKin !== undefined
    //   }
    // },
    // nextOfKinAddress: {
    //   type: String,
    //   required:function(){ // @ts-ignore
    //     return this.nextOfKin
    //   }
    // },
    // nextOfKinRelationship: {
    //   type: String,
    //   required:function(){ // @ts-ignore
    //     return this.nextOfKin
    //   }
    // },
    // profilePicture:{
    //   type: String,
    // },


    // paymentMethod:{
    //   type: String,
    //   enum:PaymentMethod,
    //   required:true
    // },
    paymentStatus:{
      type: String,
      enum:PaymentStatus,
    }
  }



export default allUserSchema