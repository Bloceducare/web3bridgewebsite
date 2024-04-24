import { z } from "zod";

export const formSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().min(2).max(50),
  number: z.string().min(2).max(50),
  country: z.string().min(2).max(50),
  city: z.string().min(2).max(50),
  address: z.string().min(2).max(50),
  type: z.enum(["male", "female"], {
    required_error: "You need to select a gender type.",
  }),
});
