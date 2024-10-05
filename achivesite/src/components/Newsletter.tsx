import React, { useState } from "react";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

toast.configure();
const Newsletter = () => {
  const [input, setInput] = useState("");

  const notify = () =>
    toast.success("you have successfully registered for our news letter!", {
      position: toast.POSITION.TOP_CENTER,
    });

  const inputHandler = (e) => {
    setInput(e.target.value);
  };
  const submitHandler = (e) => {
    e.preventDefault();
    if (input) {
      console.log(input);
      notify();
      setInput("");
    }
  };
  const iframeStyle = {
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
    maxWidth: "100%",
  };
  return (
    <div className="flex flex-col items-center justify-center bg-base py-12 mt-20">
      <div className="flex flex-col items-center justify-center">
        <h1 className=" text-white mt-7 mb-6 text-2xl font-bold text-center md:mt-0 md:text-5xl ">
          Subscribe to our Newsletter
        </h1>
        <p className=" w-11/12  m-2/5 mb-20 text-xl md:text-center text-white10 md:w-4/5 ">
          Get occasional news and update from us about the latest trends,
          technology in the web 3 world, we promise not to spam you.
        </p>
        <div>
          <iframe
            width="840"
            height="500"
            src="https://c75e802e.sibforms.com/serve/MUIFALe4lAOyLtL5vTm4hUf2XWF8FBC_TcuQ0kg1mauaBFLU8O8M5dnWtIJRiLGFZb3FDU-mU-H6Je0wsVrAV_5fBy6Xxt9j3xLoBuy_DWo7I2HJ7rNIDyBGPsBx_ZO_UDXheNqbd0vZKQiZCZBAwWNw0H0FwGt10qUK-VRlj807pjEZfs_uJqM8CK2gVfF9BL0pv9DohGVZYrwK"
            frameBorder="0"
            scrolling="auto"
            allowFullScreen
            style={iframeStyle}></iframe>
        </div>
      </div>
    </div>
  );
};

export default Newsletter;
