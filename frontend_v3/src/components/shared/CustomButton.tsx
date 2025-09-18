import { FC } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type CustomButtonTypes = {
  children: React.ReactNode;
  variant?: "default" | "outline";
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
};

const CustomButton: FC<CustomButtonTypes> = ({
  children,
  variant,
  className,
  onClick,
  disabled,
}) => {
  return (
    <Button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        variant == "default"
          ? "h-14 px-6 rounded-full border-2 ring-2 ring-red-500 border-red-300 text-red-500 font-semibold w-max"
          : "h-14 px-6 rounded-full border-2 ring-2 ring-red-200 border-red-100 text-primary w-max",
        className
      )}>
      {children}
    </Button>
  );
};

export default CustomButton;
