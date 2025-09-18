import React from "react";

const PaymentSuccess = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-5">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md text-center">
        <h1 className="text-3xl font-bold mb-4 text-green-600">
          Payment Successful
        </h1>
        <p className="text-lg text-gray-700 mb-6">
          Thank you for your payment. Your transaction was successful.
        </p>
        <button
          className="bg-red-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-700 transition duration-200"
          onClick={() =>
            (window.location.href = "https://www.web3bridgeafrica.com/")
          } // Adjust the redirection as needed
        >
          Go to Homepage
        </button>
      </div>
    </div>
  );
};

export default PaymentSuccess;
