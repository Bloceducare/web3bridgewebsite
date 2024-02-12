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

const ZkClassView = () => {
  const validationOption = validationOpt(registrationSchema.cartesi);

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
      currentTrack: Tracks.zkclass,
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
          {/* <div className="text-2xl dark:text-white20 flex flex-col items-center">
            Cartesi Masterclass Registration
            <div className="my-2 mt-3 px-3">
              <p className="text-[18px]">
                Cartesi is an app-specific rollup protocol with a virtual
                machine that runs Linux distributions, creating a richer and
                broader design space for DApp developers.
                <br /> Cartesi Rollups offer a modular scaling solution,
                deployable as L2, L3, or sovereign rollups, while maintaining
                strong base layer security guarantees.
              </p>
              <p className="text-[18px]">
                Learn more about 
                <span>
                  {" "}
                  <a
                    className="text-blue-300 underline"
                    href="https://cartesi.io/"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Cartesi
                  </a>{" "}
                </span>
                <span> and see the </span>
                <span>
                  {" "}
                  <a
                  className="text-blue-300 underline"
                    href="https://docs.cartesi.io/cartesi-rollups/build-dapps/"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    documentation
                  </a>.
                </span>
              </p>

              <p className="text-[18px]">Join our <a
                  className="text-blue-300 underline"
                    href="https://t.me/CartesiProject"
                    target="_blank"
                    rel="noopener noreferrer"
                  >Telegram</a> and <a
                  className="text-blue-300 underline"
                    href="https://discord.com/invite/pfXMwXDDfW"
                    target="_blank"
                    rel="noopener noreferrer"
                  >Discord</a> channel</p>
            </div>
          </div> */}

          <div className="text-2xl dark:text-white20 flex flex-col items-center">
            <h1 className="my-2 mt-3 px-3 text-3xl font-bold">
              ZK Masterclass Registration
            </h1>
            <p className="text-red-500 italic text-[0.8em]">Registration Ends on 20th of january 2024</p>
            <div className="my-2 mt-3 px-3">
            {!message && (
              <p className="text-[18px]">
                With the growing number of protocols and L2s implementing
                Zero-knowledge, it becomes pertinent for developers within the
                African continent to learn ZK to be relevant and contribute to
                the growth of the ecosystem. We are teaming up with protocols
                building on zero knowledge to get developers to know ZK! Join us
                for an amazing learning experience, <a href="#registration" className="font-bold text-[1em]">
                  signup here
                  </a>
                  <h1 className="font-bold text-center text-[1.2em] mt-4 italic">Requirements</h1>
                  <p className="italic font-bold">

                  Knowledge of either <span className="">
                    Rust, Go, Solidity and familiarity with linear algebra and eliptic curves would be a plus!
                    </span> 
                  </p>
              </p>
            )}
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
            <form onSubmit={handleSubmit(onSubmit)} id="registration">
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

export default ZkClassView;
