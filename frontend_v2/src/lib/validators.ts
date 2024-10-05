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
  state: z.string({ required_error: "Please enter your state" }).min(2),
  city: z.string({ required_error: "Where are you coming from?" }).min(2),
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
});
