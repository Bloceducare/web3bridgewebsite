import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { registrationSchema, validationOpt } from "schema";
import { useForm, Controller } from "react-hook-form";
import Input from "@components/commons/Input";
import Button from "@components/commons/Button";
import PhoneInput from "@components/commons/PhoneInput";
import ReactSelect from "@components/commons/ReactSelect";
import TextArea from "@components/commons/TextArea";
import { PaymentMethod, Tracks } from "enums";
import { userRegistering } from "./api";
import { CURRENT_COHORT, webPayment } from "@server/config";
import formatToCurrency from "utils/formatToCurrency";
import Select from "@components/commons/Select";
import countries from "data/countries.json";
import useCities from "./hooks/useCities";
import { PaymentStatus } from "enums";
import usePayment from "./hooks/usePayment";
import { TRAINING_CLOSED } from "config/constant";
import TrainingPyt from "@components/TrainingPyt";

const countriesData = countries.map((country) => ({
  value: country.name,
  label: country.name,
}));

const userTrack = Tracks.web3;

const Web3View = () => {
  const lazerPayConfig = {
    publicKey: process.env.NEXT_PUBLIC_LAZERPAY_PUBLIC_KEY as string,
    currency: "USD", // USD
    amount: webPayment.USD, // amount as a number
    // reference: uuidv4(), // unique identifier
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

  const router = useRouter();
  const validationOption = validationOpt(registrationSchema.web3);

  const [phone, setPhone] = useState("");
  const [error, setError] = useState<any>("");
  const [message, setMessage] = useState("");

  const handlePhoneChange = (phone) => {
    setPhone(phone);
  };

  const [retry, setRetry] = useState(false);

  const [responsePaymentStatus, setResponsePaymentStatus] = useState(
    PaymentStatus.notInitialized
  );
  const [userPaymentMethod, setUserPaymentMethod] = useState<PaymentMethod>(PaymentMethod.na)

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

  const userDetails = {
    email: watch("email"),
    name: watch("name"),
    country: watch("country"),
    city: watch("city"),
    phone: watch("phone"),
    pyt_method: watch("paymentMethod"),
  };
  userDetails.pyt_method = PaymentMethod.coupon;

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
      email: userDetails.email,
      phone_number: userDetails.phone,
      name: userDetails.name,
    },
    meta: {
      track: "web3",
    },
  });

  const onSubmit = async (value) => {
    setError("");
    setResponsePaymentStatus(PaymentStatus.notInitialized);
    setUserPaymentMethod(PaymentMethod.na)
    // if (!value.paymentMethod) {
    //   alert("Please select a payment method");
    //   return;
    // }
    if (TRAINING_CLOSED[userTrack]) {
      return alert("Registration closed !");
    }

    const data = {
      ...value,
      email: value?.email?.toLowerCase(),
      currentTrack: userTrack,
      country: value?.country?.value,
      city: value?.city?.value,
    };

    try {
      const response = await userRegistering(data);
    

      if (
        response.status === 201 &&
        PaymentMethod.card === userDetails.pyt_method
      ) {
        handlePayment({
          callback: (resp) => {
            setTimeout(() => {
              closePaymentModal();
              setMessage(response.data.message);
              window.scrollTo({ top: 0, behavior: "smooth" });
            }, 2000);
          },
          onClose: () => {},
        });
        return;
      }

      // if(response.status === 201 && data.paymentMethod === PaymentMethod.crypto){
      //   initializePaymentLazerPay()
      // }
      setMessage(response.data.message);
    } catch (e: any) {
      setError(e?.response?.data?.error ?? e.response?.data?.errors);
      setResponsePaymentStatus(e?.response?.data?.pyt);
      setUserPaymentMethod(e?.response?.data?.pytMethod);
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
            
            }, 2000);
          },
          onClose: () => {},
        });
      }
      setRetry(false);
    } catch (e) {
      setRetry(false);
    } finally {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  return (
    <>
      <div className="max-w-lg m-12 mx-auto">
        <div></div>
        <div className="flex flex-col items-center justify-center mb-6">
          <div className="text-2xl dark:text-white20">
            Cohort {CURRENT_COHORT} Registration
          </div>

          {/* <TrainingPyt
            user={userDetails}
            userTrack={userTrack}
            error={error}
            pytStatus={responsePaymentStatus}
            retry={retry}
            userPaymentMethod={userPaymentMethod}
            retryPayment={retryPayment}
          /> */}

          {!!message ? (
            <div className="my-2 text-lg text-center dark:text-white ">
              {message}
              <div className="mt-4">
                <Link href="/">
                  <a className="p-2 mt-4 text-sm font-semibold text-white bg-red-500 rounded-md">
                    Go Back Home
                  </a>
                </Link>
              </div>
            </div>
          ) : (
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
                          name="city"
                          label="City"
                          options={cities}
                          refetchOptions={() => getCities(city)}
                          optionsError={cityError}
                          placeholder={
                            cityLoadig
                              ? "Loading Cities"
                              : cities.length > 0
                              ? "Select City"
                              : "Select Country First"
                          }
                          isLoading={cityLoadig}
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
                      Technical Information
                    </legend>

                    <div>
                      <Input
                        currentValue={getValues("githubUsername")}
                        register={register}
                        disabled={isSubmitting}
                        placeholder="Bloceducare"
                        name="githubUsername"
                        required
                        label="Github Username"
                        errors={errors}
                      />
                    </div>

                    <div>
                      <Input
                        currentValue={getValues("linkedInProfile")}
                        register={register}
                        disabled={isSubmitting}
                        placeholder="https://www.linkedin.com/in/your-profile/"
                        name="linkedInProfile"
                        required
                        label="LinkedIn Profile"
                        errors={errors}
                      />
                    </div>
                  </fieldset>

                  <fieldset className="p-4 mx-2 mb-4 border rounded-md">
                    <legend className="block px-1 mb-4 text-sm font-semibold text-gray-700 uppercase dark:text-white20">
                      Other Information
                    </legend>
                    <div>
                      <Input
                        currentValue={getValues("walletAddress")}
                        register={register}
                        //  labelClassName="mb-6 border-red-500"
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
                    <div>
                      <Input
                        type="number"
                        labelClassName="mt-4 block"
                        currentValue={getValues("yearsOfExperience")}
                        register={register}
                        disabled={isSubmitting}
                        className="mt-4"
                        placeholder="Experience in months"
                        name="yearsOfExperience"
                        required
                        label="Years of Experience in months"
                        errors={errors}
                      />
                    </div>
                  </fieldset>

                  <fieldset className="p-4 mx-2 mb-4 border rounded-md">
                    <legend className="block px-1 mb-4 text-sm font-semibold text-gray-700 uppercase dark:text-white20 ">
                      Next of Kin Information
                    </legend>

                    <div>
                      <Input
                        register={register}
                        disabled={isSubmitting}
                        currentValue={getValues("nextOfKin")}
                        placeholder="John Doe"
                        name="nextOfKin"
                        required
                        label="Name"
                        errors={errors}
                      />
                    </div>

                    <div>
                      <Controller
                        control={control}
                        rules={{
                          required: true,
                        }}
                        name="nextOfKinPhone"
                        render={({ field }) => {
                          return (
                            <PhoneInput // @ts-ignore
                              value={phone}
                              disabled={isSubmitting}
                              handleChange={handlePhoneChange}
                              field={field}
                              name="nextOfKinPhone"
                              errors={errors}
                              currentValue={getValues("nextOfKinPhone")}
                            />
                          );
                        }}
                      />

                      <div>
                        <Input
                          list="nextOfKinRelation"
                          register={register}
                          disabled={isSubmitting}
                          placeholder="Enter Your Answer"
                          currentValue={getValues("nextOfKinRelationship")}
                          name="nextOfKinRelationship"
                          required
                          label="Relationship"
                          errors={errors}
                        />
                        <datalist id="nextOfKinRelation">
                          <option value="Father"></option>
                          <option value="Mother"></option>
                          <option value="Brother"></option>
                          <option value="Sister"></option>
                          <option value="Uncle"></option>
                          <option value="Aunt"></option>
                          <option value="Cousin"></option>
                          <option value="Other"></option>
                        </datalist>
                        <div>
                          <TextArea
                            name="nextOfKinAddress"
                            errors={errors}
                            register={register}
                            disabled={isSubmitting}
                            required
                            label="Address"
                            placeholder="1 Lagos street, Ikorodu Lagos"
                            currentValue={getValues("nextOfKinAddress")}
                          />
                        </div>
                      </div>
                    </div>
                  </fieldset>
                </>

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
                    )}
                    <div className="gap-2  grid grid-flow-col justify-stretch">
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
                      </div>
                      <div className=" flex items-center justify-center">
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
                      </div>

                      <div className=" flex items-center justify-center">
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
                  </div>
                    </div>
                  </div>
                </fieldset> */}

                {/* {userDetails.pyt_method === "voucher" && (
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

                <div className="px-6">
                  <Button
                    // disabled
                    disabled={!isValid || !isDirty || isSubmitting}
                    className="w-full py-3 "
                    type="submit"
                  >
                    {
                      isSubmitting ? 'Submitting' : 'Submit'
                    }
                    {/* {isSubmitting
                      ? "Loading..."
                      : userDetails.pyt_method === PaymentMethod.coupon
                      ? "Submit"
                      : `Pay Application Fee of ${
                          userDetails.pyt_method === PaymentMethod.card
                            ? `₦${new Intl.NumberFormat().format(
                                webPayment.naira
                              )}`
                            : `USD${webPayment.USD}`
                        }`} */}
                  </Button>
                </div>
              </form>
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default Web3View;
