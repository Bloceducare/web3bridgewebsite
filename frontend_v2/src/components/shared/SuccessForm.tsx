import { CheckCircle } from "lucide-react";

export default function SuccessForm() {
  return (
    <div className="max-w-[400px] md:max-w-[529px] w-full p-6 md:p-10 pt-8 bg-white dark:bg-secondary/40 rounded-xl shadow-md">
      <div className="flex gap-1 items-center justify-center text-center flex-col">
        <CheckCircle className="w-16 h-16 md:w-20 md:h-20 text-green-500 mb-3 animate-bounce" />
        <h1 className="text-lg md:text-xl font-semibold">Thank You!</h1>
        <p className="text-sm md:text-base">
          You submission has been sent successfully
        </p>
      </div>
    </div>
  );
}
