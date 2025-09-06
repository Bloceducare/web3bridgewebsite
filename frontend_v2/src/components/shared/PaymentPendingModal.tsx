"use client";

import React from "react";
import { X, CreditCard, AlertCircle, ExternalLink } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";

interface PaymentPendingModalProps {
  isOpen: boolean;
  onClose: () => void;
  message: string;
  paymentLink: string;
  participantId?: string;
}

export default function PaymentPendingModal({
  isOpen,
  onClose,
  message,
  paymentLink,
  participantId,
}: PaymentPendingModalProps) {
  if (!isOpen) return null;

  const handlePaymentClick = () => {
    window.open(paymentLink, '_blank');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 max-w-md w-full mx-4 transform transition-all duration-300 scale-100">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
        >
          <X className="w-5 h-5 text-gray-500" />
        </button>

        {/* Content */}
        <div className="p-6 pt-8">
          {/* Icon */}
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-amber-100 dark:bg-amber-900/30 rounded-full">
              <AlertCircle className="w-8 h-8 text-amber-600 dark:text-amber-400" />
            </div>
          </div>

          {/* Title */}
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white text-center mb-3">
            Payment Required
          </h3>

          {/* Message */}
          <p className="text-gray-600 dark:text-gray-300 text-center mb-6 leading-relaxed">
            {message}
          </p>

          {/* Participant ID (if available) */}
          {/* {participantId && (
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-6">
              <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
                Registration ID: <span className="font-mono font-medium">{participantId}</span>
              </p>
            </div>
          )} */}

          {/* Action buttons */}
          <div className="flex flex-col gap-3">
            <button
              onClick={handlePaymentClick}
              className={buttonVariants({ 
                variant: "bridgePrimary",
                className: "w-full flex items-center justify-center gap-2 py-3 text-base font-medium"
              })}
            >
              <CreditCard className="w-5 h-5" />
              Proceed to Payment
              <ExternalLink className="w-4 h-4" />
            </button>
            
            <button
              onClick={onClose}
              className="w-full py-3 px-4 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors font-medium"
            >
              Cancel
            </button>
          </div>

          {/* Footer note */}
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-4">
            Your registration is secure. Complete payment to confirm your spot.
          </p>
        </div>
      </div>
    </div>
  );
}
