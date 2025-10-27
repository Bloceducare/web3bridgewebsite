"use client";

import React from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Github, DollarSign, CheckCircle } from "lucide-react";

interface ZKRegistrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onProceed: () => void;
  title?: string;
}

export default function ZKRegistrationModal({
  isOpen,
  onClose,
  onProceed,
  title = "Important Registration Information"
}: ZKRegistrationModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold text-center flex items-center justify-center gap-2">
            <AlertTriangle className="w-6 h-6 text-amber-500" />
            {title}
          </DialogTitle>
          <DialogDescription className="text-center text-gray-600">
            Please read this information carefully before proceeding
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-6 py-4">
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold text-sm">1</span>
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                  Rust Programming Language Requirement
                </h3>
                <p className="text-blue-800 dark:text-blue-200 text-sm leading-relaxed">
                  This program is designed exclusively for developers who already know the Rust programming language.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0">
                <Github className="w-8 h-8 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-green-900 dark:text-green-100 mb-2">
                  GitHub Repository Review
                </h3>
                <p className="text-green-800 dark:text-green-200 text-sm leading-relaxed">
                  As part of your registration, you'll be asked to share a GitHub repository that shows your Rust projects or contributions. Our team will review your work to confirm your Rust experience before proceeding.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0">
                <DollarSign className="w-8 h-8 text-amber-600" />
              </div>
              <div>
                <h3 className="font-semibold text-amber-900 dark:text-amber-100 mb-2">
                  Payment Process
                </h3>
                <p className="text-amber-800 dark:text-amber-200 text-sm leading-relaxed">
                  Once your Rust knowledge has been verified, you'll receive a $50 payment link to finalize your registration.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0">
                <CheckCircle className="w-8 h-8 text-red-600" />
              </div>
              <div>
                <h3 className="font-semibold text-red-900 dark:text-red-100 mb-2">
                  Important Reminder
                </h3>
                <p className="text-red-800 dark:text-red-200 text-sm leading-relaxed">
                  Please ensure your GitHub profile and Rust repositories are public and accessible before you apply.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
            <div className="text-center">
              <h3 className="font-bold text-purple-900 dark:text-purple-100 mb-2">
                Ready to Join?
              </h3>
              <p className="text-purple-800 dark:text-purple-200 text-sm leading-relaxed">
                We're excited to welcome passionate Rust developers who are ready to explore Zero Knowledge technologies with us!
              </p>
            </div>
          </div>
        </div>

        <div className="flex gap-3 pt-4 border-t">
          <Button
            variant="outline"
            onClick={onClose}
            className="flex-1"
          >
            Cancel
          </Button>
          <Button
            onClick={onProceed}
            className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
          >
            I Understand, Proceed
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
