import { isOpened } from "@components/globals/TopHeader";
import { EspecializedOptions } from "enums";

export const LOCATION_BASE_URL = "https://countriesnow.space/api/v0.1/";
export const COHORT_REGISTRATION_OPENED = true;
export const SPECIAL_CLASS_OPENED = true;
export const registrationPaused = false;
export const TRAINING_CLOSED = {
  web2: !isOpened,
  web3: true,
  specialClass:false,
  cartesi: true,
  zkclass: true,
};

export const specializedClassOptions = [
  { label: "Html, CSS, intro to JavaScript", value: EspecializedOptions[0] },
  { label: "JavaScript, react, typescript", value: EspecializedOptions[1] },
  { label: "JavaScript, nodejs", value: EspecializedOptions[2] },
  { label: "GETH", value: EspecializedOptions[3] },
  { label: "Solidity", value: EspecializedOptions[4] },
];

export const trainingTime = [
  {
    label: "morning",
    value: "0",
  },
  {
    label: "evening",
    value: "1",
  },
];

// Html, CSS, intro to JavaScript

// JavaScript, react, typescript

// JavaScript, nodejs,

// GO
