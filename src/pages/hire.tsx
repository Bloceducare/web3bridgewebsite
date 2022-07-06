import React, { useState, useRef } from "react";
import Input from "../components/Input";
import { DropDown } from "../components/globals/icons";
import Image from "next/image";
import HireImage from "../../assests/hire/illustration.svg";
import type { NextPage } from "next";
import Button from "../components/Button";
import emailjs from "@emailjs/browser";

type Form = {
  fullname: string;
  email: string;
  budget: string;
  proposition: string;
};

const HireUs: NextPage = () => {
  const form: any = useRef();
  const [formData, setFormData] = useState<Form>({
    fullname: "",
    email: "",
    budget: "",
    proposition: "",
  });
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [successMessage, setSuccessMessage] = useState<string>("");
  const submitHandler = (e: any) => {
    e.preventDefault();
    if (
      !formData.budget ||
      !formData.email ||
      !formData.fullname ||
      !formData.proposition
    ) {
      return setErrorMessage("Fill All Fields !");
    }
    emailjs
      .sendForm(
        "service_9dvkucp",
        "template_b6mttgj",
        form.current,
        "5sHeJak62dtNpTbtY"
      )
      .then(
        (result) => {
          console.log(result.text);
          setSuccessMessage("Received! We will get back to you shortly!");
          setFormData({
            fullname: "",
            email: "",
            budget: "",
            proposition: "",
          });
        },
        (error) => {
          console.log(error.text);
        }
      );
  };
  const formDataHandler = (e: any, field: string) => {
    setErrorMessage("");
    setSuccessMessage("");
    const value = e.target.value;
    setFormData({ ...formData, [field]: value });
  };

  return (
    <section className="px-[1rem] md:px-[5rem] py-[5rem]">
      <div className="sm:mb-32 lg:mb-0 ml-5 sm:ml-10 md:ml-[5rem] lg:ml-0">
        <h2 className="dark:text-primary font-bold mb-1">Hire US!!!</h2>
        <h1 className="dark:text-white text-[2rem]">Lets build some magic</h1>
        <h1 className="dark:text-white text-[2rem]">together</h1>
      </div>
      <div className="flex flex-col-reverse sm:flex-row flex-wrap justify-center lg:justify-start items-start w-full mt-8">
        <div className="bg-[#FDFCFC] dark:bg-base flex flex-col items-center w-full sm:w-[80%] lg:w-[50%] px-6 py-[4rem]">
          <form ref={form} onSubmit={submitHandler}>
            <label className="self-start text-base90 dark:text-white font-bold">
              Full name
            </label>
            <Input
              changed={(e: any) => formDataHandler(e, "fullname")}
              name="full_name"
              type="text"
              value={formData.fullname}
              placeholder="Enter your full name"
            />
            <label className="self-start text-base90 dark:text-white font-bold">
              Email Address
            </label>
            <Input
              changed={(e: any) => formDataHandler(e, "email")}
              name="email"
              type="email"
              value={formData.email}
              placeholder="Enter your email address here"
            />
            <label className="self-start text-base90 dark:text-white font-bold">
              Product Type
            </label>

            <select
              className="w-full my-4 border outline-none text-white60 border-white10 rounded-md py-2 px-6 bg-[#0000] cursor-pointer"
              name="type"
              onChange={(e: any) => formDataHandler(e, "type")}
            >
              <option value="Defi">Defi</option>
              <option value="NFT">NFT</option>
              <option value="DAO'S">DAO's</option>
              <option value="Others">Others</option>
            </select>

            <label className="self-start text-base90 dark:text-white font-bold">
              Budget
            </label>
            <Input
              name="budget"
              changed={(e: any) => formDataHandler(e, "budget")}
              placeholder="Enter Your Budget"
              type="text"
              value={formData.budget}
            />
            <label className="self-start text-base90 dark:text-white font-bold">
              Unique Value Proposition (UVP)
            </label>
            <textarea
              name="prop"
              value={formData.proposition}
              onChange={(e) => formDataHandler(e, "proposition")}
              className="text-white10 px-6 py-2 w-full h-[10rem] bg-[#0000] border border-white10 rounded-md my-4"
              placeholder="Tell us more about your business idea"
            ></textarea>
            <Button
              clicked={submitHandler}
              content="SEND MESSAGE"
              type="background"
              class="w-full py-3"
            />
          </form>
          <p className="text-primary py-5">{errorMessage}</p>
          <p className="text-[#41ff83] font-bold">{successMessage}</p>
        </div>
        <div className="w-full sm:w-[80%] lg:w-[40%] flex sm:ml-[4rem] h-[20rem] mt-12 lg:mt-0 mb-20 sm:mb-0">
          <Image src={HireImage} />
          <div className="flex flex-col justify-between  h-full ">
            <div className="mt-[1rem]">
              <h1 className="text-base90 dark:text-white10 mb-4">
                Pay us a visit
              </h1>
              <p className="text-white60">
                No. 3 Abadek Avenue Ogunlewe Street, Ikorodu Lagos
              </p>
            </div>
            <div className="">
              <h1 className="text-base90 dark:text-white10 mb-4">
                Beep us on Whatsapp
              </h1>
              <p className="text-white60">Support@web3bridge.com</p>
              <p className="text-white60">+2348 109 945 686</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HireUs;
