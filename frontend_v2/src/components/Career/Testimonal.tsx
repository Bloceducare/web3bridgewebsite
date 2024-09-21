import { Card, CardContent } from "@/components/ui/card";
/* eslint-disable react/no-unescaped-entities */

export default function Testimonial() {
  return (
    <div className="bg-[#FFFBF3] dark:bg-gray-900 text-[#090808] dark:text-white py-16 px-4 sm:px-6 lg:px-8">
      <div className="sm:max-w-6xl mx-auto">
        <h2 className="text-3xl sm:text-4xl font-bold text-center mb-5 text-[#090808] dark:text-white">
          Don&apos;t just take our word!
        </h2>
        <p className="sm:text-base font-[600] text-center mb-4 text-gray-700 dark:text-gray-300">
          Here&apos;s what some of our team members have to say
        </p>
        <Card className="bg-[#FFFCF7] dark:bg-gray-800 border-0 text-black dark:text-white rounded-3xl overflow-hidden shadow-[#253A671A] dark:shadow-gray-900 shadow-lg">
          <CardContent className="p-8">
            <p className="text-base text-center leading-relaxed mb-6 text-black dark:text-gray-300">
              Joining Web3Bridge has been a transformative experience. The
              supportive and innovative environment has allowed me to expand my
              skills in blockchain development while collaborating with some of
              the brightest minds in the industry. Web3Bridge is more than just
              an organization; it&apos;s a community committed to personal
              growth, pushing boundaries, and creating impactful solutions in
              the Web3 space. I feel empowered to take on challenges and
              continuously learn, and I&apos;m proud to be part of a team
              that&apos;s shaping the future of technology.
            </p>
            <div className="text-center">
              <h3 className="font-bold text-xl mb-1 text-black dark:text-white">
                John Charles
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Product Designer
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
