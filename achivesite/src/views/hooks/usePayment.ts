import { useFlutterwave, closePaymentModal } from "flutterwave-react-v3";
import { CURRENT_COHORT } from "@server/config";

const config = {
  meta:{
    paymentFor:"trainings"
  },
  public_key: process.env.NEXT_PUBLIC_FLW_PUBLIC_KEY as string,
  tx_ref: String(Date.now()),
  currency: "NGN",
  payment_options: "card,mobilemoney,ussd",
  customizations: {
    title: `Web3Bridge Cohort ${CURRENT_COHORT}`,
    description: `Web3Bridge Cohort ${CURRENT_COHORT}`,
    logo: "https://www.web3bridge.com/web3bridge-logo.png",
    // logo: "https://st2.depositphotos.com/4403291/7418/v/450/depositphotos_74189661-stock-illustration-online-shop-log.jpg",
  },
};

const usePayment = (cardConfig) => {

  const userCardConfig = { ...config, ...cardConfig,  meta:{
    ...config.meta,
    ...cardConfig.meta
} };

  const handlePayment = useFlutterwave(userCardConfig);

  return { card: handlePayment, cardClose: closePaymentModal };
};

export default usePayment;
