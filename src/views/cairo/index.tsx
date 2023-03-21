import { useState, useEffect } from "react";
import Link from "next/link";
import { registrationSchema, validationOpt } from "schema";
import { useForm, Controller } from "react-hook-form";
import Input from "@components/commons/Input";
import Button from "@components/commons/Button";
import PhoneInput from "@components/commons/PhoneInput";
import ReactSelect from "@components/commons/ReactSelect";
import { Tracks } from "enums";
import { userRegistering } from "../api";
import Select from "@components/commons/Select";
import countries from "data/countries.json";
import useCities from "../hooks/useCities";
import { cohortList } from "data";
import { HiOutlineInformationCircle } from "react-icons/hi";

const countriesData = countries.map((country) => ({
  value: country.name,
  label: country.name,
}));

const CairoView = () => {
  const validationOption = validationOpt(registrationSchema.cairo);

  const [phone, setPhone] = useState("");
  const [error, setError] = useState<any>("");
  const [message, setMessage] = useState("");

  const handlePhoneChange = (phone) => {
    setPhone(phone);
  };

  const {
    register,
    handleSubmit,
    getValues,
    watch,
    setValue,
    control,
    formState: { errors, isSubmitting, isDirty, isValid },
    // @ts-ignore
  } = useForm<any>(validationOption);
  const userEmail = {
    email: watch("email"),
    name: watch("name"),
    country: watch("country"),
    city: watch("city"),
    alumni: watch("alumni"),
  };

  const city = getValues("country")?.value;
  const isAlumni = getValues("alumni") == "yes";

  useEffect(() => {
    setValue("city", "");
  }, [city]);
  const {
    cities,
    loading: cityLoadig,
    error: cityError,
    getCities,
  } = useCities(city);

  const onSubmit = async (value) => {
    const data = {
      ...value,
      currentTrack: Tracks.cairo,
      country: value?.country?.value,
      city: value?.city?.value,
    };

    setError("");
    try {
      const response = await userRegistering({
        ...data,
      });
      setMessage(response.data.message);
    } catch (e: any) {
      setError(
        e?.response?.data?.error ??
          e.response?.data?.errors ??
          e.response.data?.message
      );
    } finally {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  return (
    <>
      <div className="max-w-lg m-12 mx-auto">
        <div className="flex flex-col items-center justify-center mb-6">
          <div className="text-2xl dark:text-white20 flex flex-col items-center">
            Cairo Class Registration
            <div className="my-2 mt-3 px-3">
              <p className="text-[18px]">
                Cairo is a language for creating STARK-provable programs for
                general computation. Cairo powers Starknet and StarkEx, scaling
                applications on Mainnet, including dYdX, Sorare, ImmutableX, and
                more.
              </p>
              <p className="text-[18px]">
                Cairo is the native smart contract language for Starknet, a
                permissionless decentralized Validity-Rollup.
              </p>
            </div>
          </div>

          {!!error && (
            <>
              <div className="my-2 text-sm font-semibold text-red-500">
                {typeof error === "string" ? (
                  error
                ) : error?.length ? (
                  <>
                    {error.map((err: string) => (
                      <p key={err}>{err}</p>
                    ))}
                  </>
                ) : (
                  ""
                )}
              </div>
            </>
          )}
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
                          cities.length > 0
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
                      register={register}
                      disabled={isSubmitting}
                      currentValue={getValues("githubUsername")}
                      placeholder="e.g blockeducare"
                      name="githubUsername"
                      required
                      label="Github Username"
                      errors={errors}
                    />
                  </div>

                  <div>
                    <Input
                      currentValue={getValues("walletAddress")}
                      register={register}
                      disabled={isSubmitting}
                      placeholder="0x0000000000000000000000000000000000000000"
                      name="walletAddress"
                      required
                      label="Ethereum Wallet Address"
                      errors={errors}
                    >
                      <div className="-mt-4 text-sm font-primary dark:text-white20 ">
                        Don't have an ethereum wallet address?
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

                  <div className="relative mb-3 mt-3">
                    <label className="block mb-2 dark:text-white20">
                      Were you previously a graduate of the Web3bridge cohorts
                      <span className="ml-1 text-red-500">*</span>
                    </label>

                    <div className="grid grid-cols-2 mb- ">
                      <div className="">
                        <input
                          {...register("alumni")}
                          id="alumni-no"
                          type="radio"
                          disabled={isSubmitting}
                          className="form-radio"
                          name="alumni"
                          value="no"
                        />
                        <label
                          htmlFor="alumni-no"
                          className="inline-flex items-center dark:text-white10 "
                        >
                          <span className="">No</span>
                        </label>
                      </div>
                      <div className="">
                        <input
                          {...register("alumni")}
                          id="alumni-yes"
                          type="radio"
                          disabled={isSubmitting}
                          className="form-radio"
                          name="alumni"
                          value="yes"
                        />
                        <label
                          htmlFor="alumni-yes"
                          className="inline-flex items-center dark:text-white10 "
                        >
                          <span className="">Yes</span>
                        </label>
                      </div>
                    </div>
                    {(errors?.alumni?.type === "required" ||
                      !!errors?.alumni?.message) && (
                      <span className="absolute right-0 text-sm text-red-500 capitalize label-text-alt">
                        <>{errors?.alumni?.message}</>
                      </span>
                    )}
                  </div>
                  {isAlumni && (
                    <div className="relative mb-3">
                      <Select
                        labelClassName="mt-4"
                        name="prevCohort"
                        register={register}
                        disabled={isSubmitting}
                        errors={errors}
                        label="What cohort"
                        currentValue={getValues("prevCohort")}
                        options={cohortList}
                      />
                    </div>
                  )}
                </fieldset>
              </>

              <div className="px-6">
                <Button
                  disabled={!isValid || !isDirty || isSubmitting}
                  className="w-full py-3 "
                  type="submit"
                >
                  {isSubmitting ? "Loading..." : "Submit"}
                </Button>
              </div>
            </form>
          </>
        )}
      </div>
    </>
  );
};

export default CairoView;
