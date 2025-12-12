import { z } from "zod";

export const coursesSchema = z.object({
  course: z.enum(
    [
      "HTML, CSS, and JavaScript",
      "Node.js and React.js with TypeScript",
      "Solidity",
      "Go-Ethereum",
    ],
    {
      required_error: "Please select a course.",
    }
  ),
});

export const formSchema = z.object({
  name: z
    .string()
    .min(2, {
      message: "Name must be at least 2 characters.",
    })
    .max(30, {
      message: "Name must be less than 30 characters.",
    }),
  email: z.string({ required_error: "Please enter your email address" }).min(2),
  number: z
    .string({ required_error: "Please enter your phone number" })
    .min(2)
    .max(50),
  github: z
    .string({ required_error: "Github profile link is required" })
    .min(2),
  country: z.string({ required_error: "Please enter your country" }).min(2),
  venue: z.string({ required_error: "Please enter your venue" }).min(2),
  state: z.string({ required_error: "Please enter your state" }).min(2),
  city: z.string({ required_error: "Where are you coming from?" }).min(2),
  cohort: z.string({ required_error: "cohort" }).min(3),
  gender: z.enum(["male", "female"], {
    required_error: "You need to select a gender type.",
  }),
});

export const otherSchema = z.object({
  duration: z.string().max(30),
  motivation: z.string().min(2).max(1000),
  achievement: z.string().min(2).max(1000),
  wallet_address: z
    .string({ required_error: "Please enter your wallet address" })
    .min(2),
  discount: z.string().optional(),
  cta: z.boolean().refine((val) => val === true, {
    message: "You must agree to the terms before proceeding.",
  }),
});

export const hubRegistrationSchema = z.object({
  name: z
    .string()
    .min(2, {
      message: "Name must be at least 2 characters.",
    })
    .max(255, {
      message: "Name must be less than 255 characters.",
    }),
  email: z
    .string({ required_error: "Please enter your email address" })
    .email("Please enter a valid email address")
    .min(2),
  phone_number: z
    .string({ required_error: "Please enter your phone number" })
    .min(2)
    .max(20),
  location: z
    .string({ required_error: "Please enter your location" })
    .min(2)
    .max(255),
  reason: z
    .string({ required_error: "Please explain why you want to use the hub" })
    .min(10, {
      message: "Please provide a more detailed reason (at least 10 characters).",
    })
    .max(2000),
  role: z
    .string({ required_error: "Please describe your role in the ecosystem" })
    .min(2)
    .max(255),
  contribution: z
    .string({ required_error: "Please share how you contribute to Ethereum" })
    .min(10, {
      message: "Please provide more details about your contribution (at least 10 characters).",
    })
    .max(2000),
  preferred_date: z
    .string({ required_error: "Please select a preferred date" })
    .min(1, "Please select a preferred date"),
  preferred_time: z
    .string({ required_error: "Please select a preferred time" })
    .min(1, "Please select a preferred time"),
  expected_duration_hours: z
    .number()
    .min(1, "Duration must be at least 1 hour")
    .max(12, "Duration cannot exceed 12 hours")
    .default(4)
    .optional(),
});
