import { CURRENT_COHORT } from "@server/config";
import { PaymentMethod, PaymentStatus } from "enums";
import Button from "./commons/Button";

const TrainingPyt = ({
  retry,
  retryPayment,
  pytStatus,
  error,
  userTrack,
  user,
  userPaymentMethod=PaymentMethod.na
}) => {

  return (
    <>
      {!!error ? (
        <div className="my-2 text-sm font-semibold text-red-500 text-center">
          {typeof error === "string" ? (
            error
          ) : error?.length ? (
            <>
              {error.map((err: string) => (
                <p key={err}>{err}</p>
              ))}
            </>
          ) : null}

          {pytStatus === PaymentStatus.success && PaymentMethod.coupon !==userPaymentMethod && (
            <div className="dark:text-white20 mt-2 font-normal max-w-xs">
              We have received your payment, relax and expect to hear from us
              soon!
            </div>
          )}

          {pytStatus === PaymentStatus.pending && (
            <div>
              <p>Payment pending, please try again</p>
              <Button
                disabled={retry}
                type="button"
                onClick={() => retryPayment(user?.pyt_method)}
                className="p-2 mx-2 mt-4 text-sm font-semibold text-white bg-red-500 rounded-md"
              >
                {retry ? "Paying..." : "Retry Payment"}
              </Button>
              <div className="dark:text-white20 mt-2 font-normal">
                If you feel this is not correct, Please Send us a Message{" "}
                <a
                  className="dark:text-rose-300 underline"
                  href={`mailto:support@web3bridge.com?subject=Training Payment not Recorded&body=Hello\n I'm reaching out because I make an payment for Cohort ${CURRENT_COHORT} 2023 ${userTrack}, I have been debited but I am getting the error payment still pending\n Here are my details;\n Name:${user?.name},\n Email:${user?.email}\n Payment Method:${user?.pyt_method}\n I look forward to hear from you.\n Thanks\n ${user?.name}`}
                >
                  support[at]web3bridge.com
                </a>{" "}
              </div>
            </div>
          )}
        </div>
      ) : null}
    </>
  );
};

export default TrainingPyt;
