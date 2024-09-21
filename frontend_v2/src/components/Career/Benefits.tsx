import { Card, CardContent } from "@/components/ui/card";
import { benefitsData } from "@/data/Career";
import Image from "next/image";
/* eslint-disable react/no-unescaped-entities */

export default function Benefits() {
  return (
    <main className="bg-[#FFFBF3] dark:bg-gray-900">
      <div className="max-w-6xl mx-auto px-4 pt-12">
        <div className="max-w-[43rem] mx-auto">
          <h1 className="text-4xl font-bold text-center mb-4 text-[#090808] dark:text-white">
            What benefits are waiting for you?
          </h1>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-8">
            We want our employees to feel supported and appreciated. That&apos;s
            why we offer a range of benefits designed to enhance your career and
            life.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {benefitsData.map((benefit, index) => (
            <Card
              key={index}
              className={`${benefit.bgColor} dark:bg-gray-800 rounded-[1rem] rounded-b-none p-[2px] border-2 border-b-0 dark:border-gray-700 shadow-lg`}>
              <CardContent className="flex flex-col items-center justify-center p-6">
                <Image
                  src={benefit.icon}
                  alt={`${benefit.title} icon`}
                  className="dark:invert"
                />
                <h3 className="mt-4 text-black dark:text-white tracking-wider text-base max-w-[9rem] font-[600] text-center">
                  {benefit.title}
                </h3>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </main>
  );
}
