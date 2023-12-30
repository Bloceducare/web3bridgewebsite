import { string, object, array, mixed, ref } from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { EClassCat, PaymentMethod, Tracks } from "enums";
import countries from "data/countries.json";
import showTime from "utils/showTimePeriods";

const mappedCountries = countries.map((country) => country.name);

export function validationOpt(schema, options = {}) {
  return { mode: "all", resolver: yupResolver(schema), ...options };
}

export const mainSchema = object().shape({
  voucher: string()
    // .required("voucher is required")
    .length(6, "incorrect voucher"),
  name: string()
    .required("Name is required")
    .min(8, "Name length should be at least 4 characters"),
  email: string()
    .required("Email is required")
    .matches(
      /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,5})+$/,
      "Email is not valid"
    ),
  gender: string().required("Gender is required").nullable(),
  phone: string()
    .required("Phone is required")
    .matches(/^[0-9]{4,15}$/, "Phone number is not valid"),
  country: object()
    .shape({
      label: string(),
      value: string()
        .required("Country is required")
        .oneOf(mappedCountries, "Country is not valid"),
    })
    .nullable(),
  city: object()
    .shape({
      label: string(),
      value: string()
      // .required("City is required"),
    })
    .nullable(),

  // walletAddress: string()
  //   .required("Wallet Address is required")
  //   .matches(/^0x[a-fA-F0-9]{40}$/, 'Wallet Address is not valid'),
  paymentMethod: mixed<PaymentMethod>()
    .oneOf(Object.values(PaymentMethod), "Payment method is not valid")
    // .required("Payment method is required")
    .nullable(),
});

export const userTypeSchema = object().shape({
  currentTrack: string()
    .required("Current track is required")
    .oneOf(Object.values(Tracks), "Current track is not valid")
    .nullable(),
});
const paymentSchema = object().shape({
  paymentMethod: mixed<PaymentMethod>()
    .oneOf(Object.values(PaymentMethod), "Payment method is not valid")
    .required("Payment method is required")
    .nullable(),
});

export const initPaymentSchema = object().shape({
  reference: string().required("Reference is required"),
  email: string().required("Email is required"),
  paymentMethod: string().required("Payment method is required"),
});

export const dailyCommitmentSchema = object().shape({
  twoHrMinDailyCommitment: string()
    .required("Response is required")
    .oneOf(["yes", "no", "maybe"], "Response is not valid"),
});

export const inspirationForCodingSchema = object().shape({
  inspirationForCoding: string()
    .required("Response is required")
    .min(10, "Response length should be at least 10 characters"),
});

export const achievementFromProgramSchema = object().shape({
  achievementFromProgram: string()
    .required("Response is required")
    .min(10, "Response length should be at least 10 characters"),
});

export const verifyPaymentSchema = object().shape({
  reference: string().required("Reference is required"),
  email: string().required("Email is required").email("Email is not valid"),
});

const githubSchema = object().shape({
  githubUsername: string()
    .required("Github Username is required")
    .min(3, "Github Username length should be at least 3 characters"),
});
const technicalSchema = githubSchema.concat(
  object().shape({
    progLang: array().min(1, "Please select at least one programming language"),
  })
);

const yearsOfExperienceSchema = object().shape({
  yearsOfExperience: string().required("Month of experience is required"),
});

const walletSchema = object().shape({
  walletAddress: string()
    .required("Wallet Address is required")
    .matches(/^0x[a-fA-F0-9]{40}$/, "Wallet Address is not valid"),
});

const nextOfKinSchema = object().shape({
  nextOfKin: string()
    .required("Next of Kin is required")
    .min(4, "Next of Kin length should be at least 4 characters"),
  nextOfKinPhone: string()
    .required("Next of Kin Phone is required")
    .matches(/^[0-9]{4,15}$/, "Phone number is not valid")
    .notOneOf(
      [ref("nextOfKin"), null],
      "next of kin phone cannot be the same as your phone number"
    ),
  nextOfKinAddress: string()
    .required("Next of Kin Address is required")
    .min(4, "Next of Kin Address length should be at least 4 characters"),
  nextOfKinRelationship: string()
    .required("Next of Kin Relationship is required")
    .min(3, "Next of Kin Relationship length should be at least 4 characters"),
});

const linkedInProfileSchema = object().shape({
  linkedInProfile: string().required("LinkedIn Profile is required"),
});

const areaOfInterestSchema = object().shape({
  AreaOfInterest: string().required("Area of Interest is required"),
});

export const couponSchema = object().shape({
  identifier: string().required("coupon identifier is needed"),
  email: string()
    .required("Email is required")
    .matches(
      /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,5})+$/,
      "Email is not valid"
    ),
});

export const alumniSchema = object().shape({
  alumni: string().required("Alumni Status is required").nullable(),
  prevCohort: mixed().test(
    "alumni",
    "Cohort Class is required",
    (value, ot) => {
      const isAlumni = ot.parent.alumni == "yes";
      if (isAlumni && !!!value) return false;
      return true;
    }
  ),
});

const timeSchema = object().shape({
  trainingTime: string().when("AreaOfInterest", {
    is: (details) => {
      return showTime(details);
    },
    then: string().required("time field is required"),
  }),
});

const web2ClassCatSchema = object().shape({
  classCat: mixed<EClassCat>()
    .oneOf(Object.values(EClassCat), "Category is not valid")
    .required("Training Category is required")
    .nullable(),
});

export const registrationSchema = {
  web2: mainSchema
    .concat(achievementFromProgramSchema)
    .concat(inspirationForCodingSchema)
    .concat(dailyCommitmentSchema)
    .concat(walletSchema)
    .concat(web2ClassCatSchema),
  web3: mainSchema
    .concat(technicalSchema)
    .concat(nextOfKinSchema)
    .concat(walletSchema)
    .concat(yearsOfExperienceSchema)
    .concat(linkedInProfileSchema),
  specialClass: mainSchema
    .concat(areaOfInterestSchema)
    .concat(paymentSchema)
    .concat(timeSchema),
  cartesi: mainSchema
    .concat(walletSchema)
    .concat(githubSchema)
    .concat(alumniSchema),
  zkclass: mainSchema
    .concat(walletSchema)
    .concat(githubSchema)
    .concat(alumniSchema),
};
