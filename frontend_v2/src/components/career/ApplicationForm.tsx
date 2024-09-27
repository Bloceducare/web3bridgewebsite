"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function ApplicationForm() {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log("Form submitted");
  };

  return (
    <Card className="w-full border-0 shadow-none max-w-2xl mx-auto bg-[#FFF3F3] dark:bg-gray-800">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center text-black dark:text-white">
          Application Portal
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="fullName" className="text-black dark:text-white">
              Full name *
            </Label>
            <Input
              id="fullName"
              className="rounded-[2rem] shadow-[#FF9393] dark:bg-gray-700 dark:text-white"
              placeholder="Full name"
              required
            />
          </div>
          <div>
            <Label htmlFor="email" className="text-black dark:text-white">
              Email *
            </Label>
            <Input
              id="email"
              type="email"
              className="rounded-[2rem] shadow-[#FF9393] dark:bg-gray-700 dark:text-white"
              placeholder="Email"
              required
            />
          </div>
          <div>
            <Label htmlFor="phone" className="text-black dark:text-white">
              Phone number *
            </Label>
            <Input
              id="phone"
              type="tel"
              className="rounded-[2rem] shadow-[#FF9393] dark:bg-gray-700 dark:text-white"
              placeholder="Phone number"
              required
            />
          </div>
          <div className="flex space-x-4">
            <div className="flex-1">
              <Label htmlFor="role" className="text-black dark:text-white">
                Role/Position *
              </Label>
              <Input
                id="role"
                className="rounded-[2rem] shadow-[#FF9393] dark:bg-gray-700 dark:text-white"
                placeholder="Job Role/Position"
                required
              />
            </div>
            <div className="flex-1">
              <Label
                htmlFor="employmentType"
                className="text-black dark:text-white"
              >
                Employment type *
              </Label>
              <Select required>
                <SelectTrigger className="rounded-[2rem] shadow-[#FF9393] dark:bg-gray-700 dark:text-white">
                  <SelectValue placeholder="Full time" />
                </SelectTrigger>
                <SelectContent className="dark:bg-gray-700 dark:text-white">
                  <SelectItem value="fullTime">Full time</SelectItem>
                  <SelectItem value="partTime">Part time</SelectItem>
                  <SelectItem value="contract">Contract</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="flex space-x-4">
            <div className="flex-1">
              <Label htmlFor="location" className="text-black dark:text-white">
                Location *
              </Label>
              <Input
                id="location"
                className="rounded-[2rem] shadow-[#FF9393] dark:bg-gray-700 dark:text-white"
                placeholder="Current Location"
                required
              />
            </div>
            <div className="flex-1">
              <Label htmlFor="cv" className="text-black dark:text-white">
                CV/Resume/Cover Letter *
              </Label>
              <div className="flex items-center space-x-2">
                <Input
                  id="cv"
                  type="file"
                  className="hidden"
                  onChange={handleFileChange}
                  accept=".pdf,.doc,.docx"
                  required
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => document.getElementById("cv")?.click()}
                  className="w-full rounded-[2rem] shadow-[#FF9393] dark:bg-gray-700 dark:text-white"
                >
                  {file ? file.name : "Select a file"}
                </Button>
                {file && (
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={() => setFile(null)}
                    className="px-2 dark:text-white"
                  >
                    ✕
                  </Button>
                )}
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                PDF file size no more than 10MB
              </p>
            </div>
          </div>
          <Button
            type="submit"
            className="rounded-full w-full px-12 py-6 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 dark:bg-red-500/20 text-bridgeRed dark:text-white hover:bg-transparent dark:hover:bg-transparent"
          >
            Submit Application
          </Button>
          <p className="text-xs text-center text-gray-500 dark:text-gray-400">
            By clicking{" "}
            <span className="text-[#E62727] dark:text-red-400 font-[700]">
              Submit application
            </span>
            , you agree to our Privacy Policy and Cookie Policy.
          </p>
        </form>
      </CardContent>
    </Card>
  );
}
