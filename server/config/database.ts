import mongoose from "mongoose";

const connectDB = async () => {
  try {
    const connect = await mongoose.connect(`${process.env.DB_CREDENTIALS}`);
    // console.log(`Database connected to ${connect.connection.host}`);
    return connect.connection.host;
  } catch (error) {
    console.log(error);
  }
};

export default connectDB;

export const closeDB = async () => {
  try {
    return await mongoose.connection.close();
  } catch {}
};
