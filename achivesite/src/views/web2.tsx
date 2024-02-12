import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { useRouter } from "next/router";
import Link from "next/link";
import { registrationSchema, validationOpt } from "schema";
import { useForm, Controller } from "react-hook-form";
import Input from "@components/commons/Input";
import Button from "@components/commons/Button";
import PhoneInput from "@components/commons/PhoneInput";
import ReactSelect from "@components/commons/ReactSelect";
import TextArea from "@components/commons/TextArea";
import { Gender, PaymentMethod, PaymentStatus, Tracks } from "enums";
import { userRegistering } from "./api";
import { CURRENT_COHORT, webPayment } from "@server/config";
import formatToCurrency from "utils/formatToCurrency";
import Select from "@components/commons/Select";
import countries from "data/countries.json";
import useCities from "./hooks/useCities";
import usePayment from "./hooks/usePayment";
import { TRAINING_CLOSED } from "config/constant";
import TrainingPyt from "@components/TrainingPyt";
import Tooltip from "@components/commons/Tooltip";

const userTrack = Tracks.web2;
const countriesData = countries.map((country) => ({
  value: country.name,
  label: country.name,
}));

const Web2View = () => {
  const router = useRouter();

  const lazerPayConfig = {
    publicKey: process.env.NEXT_PUBLIC_LAZERPAY_PUBLIC_KEY as string,
    currency: "USD", // USD, NGN, AED, GBP, EUR
    amount: webPayment.USD, // amount as a number or string
    reference: uuidv4(), // unique identifier
    metadata: {
      track: userTrack,
    },
    onSuccess: (response) => {
      // handle response here
      router.push("/");
    },
    onClose: () => {
      //handle response here
    },
    onError: (response) => {
      // handle responsne here
    },
  };

  const config = {
    reference: uuidv4(),
    amount: webPayment.naira,
    publicKey: process.env.NEXT_PUBLIC_PAYMENT_PUBLIC_KEY as string,
  };

  //
  const validationOption = validationOpt(registrationSchema.web2);

  const [phone, setPhone] = useState("");
  const [error, setError] = useState<any>("");
  const [message, setMessage] = useState("");
  const [responsePaymentStatus, setResponsePaymentStatus] = useState(
    PaymentStatus.notInitialized
  );

  const [userPaymentMethod, setUserPaymentMethod] = useState(PaymentMethod.na);

  const handlePhoneChange = (phone) => {
    setPhone(phone);
  };
  const [retry, setRetry] = useState(false);
  const {
    register,
    handleSubmit,
    getValues,
    watch,
    setValue,
    control,
    formState: { errors, isSubmitting: formSubmitting, isDirty, isValid },

    // @ts-ignore
  } = useForm<any>(validationOption);

  const isSubmitting = retry || formSubmitting;

  const userEmail = {
    email: watch("email"),
    name: watch("name"),
    country: watch("country"),
    city: watch("city"),
    pyt_method: watch("paymentMethod"),
    phone: watch("phone"),
  };

  // userEmail.pyt_method = PaymentMethod.card;
  const city = getValues("country")?.value;

  useEffect(() => {
    setValue("city", "");
  }, [city]);

  const {
    cities,
    loading: cityLoadig,
    error: cityError,
    getCities,
  } = useCities(city);

  const { card: handlePayment, cardClose: closePaymentModal } = usePayment({
    amount: webPayment.naira,
    customer: {
      email: userEmail.email,
      phone_number: userEmail.phone,
      name: userEmail.name,
    },
    meta: {
      track: "web2",
    },
  });

  const onSubmit = async (value) => {
    const data = {
      ...value,
      currentTrack: userTrack,
      country: value?.country?.value,
      city: value?.city?.value,
    };

    setError("");
    // setUserPaymentMethod(PaymentMethod.na);
    // setResponsePaymentStatus(PaymentStatus.notInitialized);
    if (TRAINING_CLOSED[userTrack]) {
      return alert("Registration closed!");
    }

    try {
      const response = await userRegistering(data);

      // if (
      //   response.status === 201 &&
      //   userEmail.pyt_method === PaymentMethod.card
      // ) {
      //   handlePayment({
      //     callback: () => {
      //       setTimeout(() => {
      //         closePaymentModal();

      //         setMessage(response.data.message);
      //         window.scrollTo({ top: 0, behavior: "smooth" });
      //       }, 2000);
      //     },
      //     onClose: () => {},
      //   });
      //   return;
      // }

      // if(response.status === 201 && data.paymentMethod === PaymentMethod.crypto){
      //   initializePaymentLazerPay()
      // }
      setMessage(response.data.message);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (e: any) {
      const isError = e?.response?.data?.error ?? e.response?.data?.errors;
      setError(!!isError ? isError : "An Error Occurred, Try again");
      // setResponsePaymentStatus(e?.response?.data?.pyt);
      // setUserPaymentMethod(e?.response?.data?.pytMethod);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const retryPayment = async (payment) => {
    setRetry(false);

    try {
      setRetry(true);
      if (payment === PaymentMethod.card) {
        handlePayment({
          callback: () => {
            setTimeout(() => {
              setError("");
              setResponsePaymentStatus(PaymentStatus.notInitialized);
              closePaymentModal();
              setMessage(
                "Payment Successful, Please check Your Email for Further Instructions"
              );
              window.scrollTo({ top: 0, behavior: "smooth" });
            }, 2000);
          },
          onClose: () => {},
        });
      }
      setRetry(false);
    } catch (e) {
      setRetry(false);
    }
  };
  return (
    <>
      <div className="max-w-lg m-12 mx-auto">
        <div></div>
        <div className="flex flex-col items-center justify-center mb-6 text-center">
          <div className="text-2xl dark:text-white20">
            Cohort {CURRENT_COHORT} Registration
          </div>
          {/* <TrainingPyt
            user={userEmail}
            userTrack={userTrack}
            error={error}
            pytStatus={responsePaymentStatus}
            retry={retry}
            retryPayment={retryPayment}
            userPaymentMethod={userPaymentMethod}
          /> */}

          {!!message && (
            <div className="my-2 text-lg text-center capitalize dark:text-white ">
              {message}
              <div className="mt-4">
                <Link href="/">
                  <a className="p-2 mt-4 text-sm font-semibold text-white bg-red-500 rounded-md ">
                    Go Back Home
                  </a>
                </Link>
              </div>
            </div>
          )}
        </div>
        {!message && (
          <>
            <form onSubmit={handleSubmit(onSubmit)}>
              <fieldset className="p-4 mx-2 mb-4 border rounded-md">
                <legend className="block px-1 mb-4 text-sm font-semibold text-gray-700 uppercase dark:text-white20">
                  Personal Information
                </legend>

                <div>
                  <Input
                    register={register}
                    disabled={isSubmitting}
                    currentValue={getValues("name")}
                    placeholder="Jane Doe"
                    name="name"
                    required
                    label="Name"
                    errors={errors}
                  />
                </div>
                <div>
                  <Input
                    currentValue={getValues("email")}
                    register={register}
                    disabled={isSubmitting}
                    placeholder="janedoe@mail.com"
                    name="email"
                    required
                    label="Email"
                    errors={errors}
                  />
                </div>
                <div className="relative mb-3">
                  <Select
                    name="gender"
                    register={register}
                    disabled={isSubmitting}
                    errors={errors}
                    label="Gender"
                    currentValue={getValues("gender")}
                    options={[
                      { label: "male", value: "male" },
                      { label: "female", value: "female" },
                    ]}
                  />
                </div>

                <div>
                  <Controller
                    control={control}
                    rules={{
                      required: true,
                    }}
                    name="phone"
                    render={({ field }) => {
                      return (
                        <PhoneInput // @ts-ignore
                          value={phone}
                          disabled={isSubmitting}
                          handleChange={handlePhoneChange}
                          field={field}
                          name="phone"
                          errors={errors}
                          currentValue={getValues("phone")}
                        />
                      );
                    }}
                  />
                </div>

                <div className="relative mb-4">
                  <Controller
                    name="country"
                    control={control}
                    render={({ field }) => (
                      <ReactSelect
                        field={field}
                        name="country"
                        label="Country"
                        disabled={isSubmitting}
                        options={countriesData}
                        value={getValues("country")?.value}
                        placeholder="Select Country"
                        optionsError={false}
                        errors={errors}
                      />
                    )}
                  />
                </div>

                <div className="relative mb-4">
                  <Controller
                    name="city"
                    control={control}
                    render={({ field }) => (
                      <ReactSelect
                        field={field}
                        errors={errors}
                        name="city"
                        label="City"
                        options={cities}
                        placeholder={
                          cityLoadig
                            ? "Loading Cities"
                            : cities.length > 0
                            ? "Select City"
                            : "Select Country First"
                        }
                        isLoading={cityLoadig}
                        refetchOptions={() => getCities(city)}
                        optionsError={cityError}
                        value={getValues("city")?.value}
                        disabled={
                          (!!getValues("country")?.value ? false : true) ||
                          isSubmitting
                        }
                      />
                    )}
                  />
                </div>
              </fieldset>

              <>
                <fieldset className="p-4 mx-2 mb-4 border rounded-md">
                  <legend className="block px-1 mb-4 text-sm font-semibold text-gray-700 uppercase dark:text-white20">
                    Other Information
                  </legend>
                  <div>
                    <Input
                      currentValue={getValues("walletAddress")}
                      register={register}
                      disabled={isSubmitting}
                      placeholder="0x0000000000000000000000000000000000000000"
                      name="walletAddress"
                      required
                      label="ERC20 address (Metamask or any other decentralised wallet address)"
                      errors={errors}
                    >
                      <div className="-mt-4 text-sm font-primary dark:text-white20 ">
                        Don't have a wallet address?
                        <a
                          href="https://drive.google.com/file/d/11RLyQcbFUV2A7KViksOAihhRi1Iz9EVB/view"
                          target="_blank"
                          className="ml-1 text-blue-500 underline capitalize"
                        >
                          learn more
                        </a>
                      </div>
                    </Input>
                  </div>

                  <div className="relative my-5">
                    <label className="block mb-2 dark:text-white20">
                      <Tooltip text={<ClassCat />}>
                        What Category will you like to apply for
                      </Tooltip>
                    </label>
                    {(errors?.classCat?.type === "required" ||
                      !!errors?.classCat?.message) && (
                      <span className="absolute right-0 text-sm text-red-500 capitalize label-text-alt">
                        <>{errors?.classCat?.message}</>
                      </span>
                    )}
                    <div className="gap-2  grid grid-flow-col justify-stretch">
                      <div className="flex items-center justify-center">
                        <input
                          {...register("classCat")}
                          id="classCat-basic"
                          type="radio"
                          disabled={isSubmitting}
                          className="form-radio"
                          name="classCat"
                          value="basic"
                        />
                        <label
                          htmlFor="classCat-basic"
                          className="inline-flex items-center dark:text-white10  "
                        >
                          <span className="">Beginner</span>
                        </label>
                      </div>
                      <div className=" flex items-center justify-center">
                        <input
                          {...register("classCat")}
                          id="classCat-advanced"
                          type="radio"
                          disabled={isSubmitting}
                          className="form-radio"
                          name="classCat"
                          value="advanced"
                        />
                        <label
                          htmlFor="classCat-advanced"
                          className="inline-flex items-center dark:text-white10 "
                        >
                          <span className="">Advanced</span>
                        </label>
                      </div>
                    </div>
                  </div>

                  <div className="relative mb-5">
                    <Select
                      labelClassName="mt-4"
                      name="twoHrMinDailyCommitment"
                      register={register}
                      disabled={isSubmitting}
                      errors={errors}
                      label="Will you be able to commit minimum of 2 hours daily to learning?"
                      currentValue={getValues("twoHrMinDailyCommitment")}
                      options={[
                        { label: "Yes", value: "yes" },
                        { label: "No", value: "no" },
                        { label: "Maybe", value: "maybe" },
                      ]}
                    />
                  </div>

                  <div className="relative mb-3">
                    <TextArea
                      label="What is your motivation and inspiration to start writing code?"
                      register={register}
                      disabled={isSubmitting}
                      name="inspirationForCoding"
                      errors={errors}
                      currentValue={getValues("inspirationForCoding")}
                      required
                    />
                  </div>
                  <div className="relative mb-3">
                    <TextArea
                      label="What do you hope to achieve from this program?"
                      register={register}
                      disabled={isSubmitting}
                      name="achievementFromProgram"
                      errors={errors}
                      currentValue={getValues("achievementFromProgram")}
                      required
                    />
                  </div>
                </fieldset>
              </>

              <>
                {/* <fieldset className="p-4 mx-2 mb-4 border rounded-md">
                  <legend className="block px-1 mb-4 text-sm font-semibold text-gray-700 uppercase dark:text-white20">
                    Payment
                  </legend>
                  <div className="relative mb-3">
                    <label className="block mb-2 dark:text-white20">
                      Payment Method (
                      {`₦${formatToCurrency(
                        webPayment.naira
                      )}/$${formatToCurrency(webPayment.USD)}`}
                      )<span className="ml-1 text-red-500">*</span>
                    </label>
                    {(errors?.paymentMethod?.type === "required" ||
                      !!errors?.paymentMethod?.message) && (
                      <span className="absolute right-0 text-sm text-red-500 capitalize label-text-alt">
                        <>{errors?.paymentMethod?.message}</>
                      </span>
                    )} */}
                {/* <div className="gap-2  grid grid-flow-col justify-stretch">
                      <div className="flex items-center justify-center">
                        <input
                       
                       {...register("paymentMethod")}
                          id="paymentMethod-card"
                          type="radio"
                          disabled={isSubmitting}
                          className="form-radio"
                          name="paymentMethod"
                          value="card"
                        />
                        <label
                          htmlFor="paymentMethod-card"
                          className="inline-flex items-center dark:text-white10  "
                        >
                          <span className="">Card</span>
                        </label>
                      </div> */}
                {/* <div className=" flex items-center justify-center">
                        <input
                          {...register("paymentMethod")}
                          id="paymentMethod-crypto"
                          type="radio"
                          disabled={isSubmitting}
                          className="form-radio"
                          name="paymentMethod"
                          value="crypto"
                        />
                        <label
                          htmlFor="paymentMethod-crypto"
                          className="inline-flex items-center dark:text-white10 "
                        >
                          <span className="">Crypto</span>
                        </label>
                      </div> */}

                {/* <div className=" flex items-center justify-center">
                        <input
                        {...register("paymentMethod")}
                        
                          id="paymentMethod-voucher"
                          type="radio"
                          disabled={isSubmitting}
                          className="form-radio"
                          name="paymentMethod"
                          value="voucher"
                        />
                        <label
                          htmlFor="paymentMethod-voucher"
                          className="inline-flex items-center dark:text-white10 "
                        >
                          <span className="">Voucher</span>
                        </label>
                      </div> */}
                {/* </div> */}
                {/* </div>
                </fieldset> */}

                {/* {userEmail.pyt_method === "voucher" && (
                  <>
                    {" "}
                    <fieldset className="p-4 mx-2 mb-4 border rounded-md">
                      <legend className="block px-1 mb-4 text-sm font-semibold text-gray-700 uppercase dark:text-white20">
                        Apply Voucher
                      </legend>
                      <div className="relative mb-3">
                        <Input
                          lowerCase={false}
                          register={register}
                          disabled={isSubmitting}
                          currentValue={getValues("voucher")}
                          placeholder="Enter a valid voucher"
                          name="voucher"
                          label="Voucher"
                          errors={errors}
                        />
                      </div>
                    </fieldset>
                  </>
                )} */}
              </>

              <div className="px-6">
                <Button
                  disabled={!isValid || !isDirty || isSubmitting}
                  className="w-full py-3 "
                  type="submit"
                >
                  {
                    isSubmitting ? "Submitting....." : "Submit"
                    // : userEmail.pyt_method === PaymentMethod.card ? `Pay Application Fee of ₦${new Intl.NumberFormat().format(
                    // webPayment.naira
                    // )}` :userEmail.pyt_method === PaymentMethod.coupon ? "Pay Application Fee of ₦0.00" :`Choose Payment Method `
                  }
                </Button>
              </div>
            </form>
          </>
        )}
      </div>
    </>
  );
};

export default Web2View;

export const ClassCat = () => {
  return (
    <div>
      <div className="mb-2">
        <span className="underline"> Beginner</span>
        <div>
          You are not comfortable with html css and/or barely used Javascript.
          Heck, you don't even know what those means.
        </div>
      </div>
      <div>
        <span className="underline"> Advanced</span>
        <div>
          You have some experience with html, css and javascript and you're
          comfortable building a simple weather app
        </div>
      </div>
    </div>
  );
};
