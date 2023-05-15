import axios from "axios";

export const userRegistering = async (data) => {
  const user = await axios.post("/api/cohort-users", data);
  return user;
};

export const specialClassRegistering = async (data) => {
  const user = await axios.post("/api/special-class", data);
  return user;
};

export const getTotalLeft = async (track, typeOfTrack) => {
  if (track != "specialClass") return null;
  const { data } = await axios.get(`/api/special-class?type=${typeOfTrack}`);
  return data ?? null;
};

export const initPayment = async (data) => {
  const payment = await axios.post("/api/init-payment", data);
  return payment;
};

export const verifyPayment = async (data) => {
  try {
    const payment = await axios.post("/api/verify-payment", data);
    return payment;
  } catch (e: any) {
    throw e.response.data;
  }
};

export const getUser = async (data) => {
  const { email, currentTrack } = data;
  try {
    const response = await axios.get(
      `/api/cohort-users?email=${email}&currentTrack=${currentTrack}`,
      data
    );
    return response?.data?.data;
  } catch (e: any) {
    throw e.response.data;
  }
};
