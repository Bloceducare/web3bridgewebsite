import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva("inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default:
          " text-primary-foreground rounded-md shadow hover:bg-primary/90 shadow-[inset_1px_1px_8px_#FFC7E1]",
        destructive:
          " text-destructive-foreground rounded-md shadow-sm hover:bg-destructive/90",
        outline:
          " rounded-full shadow-sm dark: hover:bg-accent hover:text-accent-foreground shadow-[inset_1px_1px_8px_#FFC7E1]",
        secondary:
          "rounded-full bg-[rgba(234,13,83,0.03)] px-12 py-6 text-primary-background capitalize  shadow-[inset_1px_1px_18px_rgba(255,148,198,0.37)] dark:text-primary",
        ghost: "rounded-md hover:bg-accent hover:text-accent-foreground",
        link: "text-primary rounded-md underline-offset-4 hover:underline",
        bridgePrimary:
          "rounded-full bg-bridgeRed px-12 py-6 text-primary-foreground capitalize  shadow-[inset_1px_1px_18px_#FFC7E1] dark:text-primary",
        bridgeOutline: "rounded-full px-12 py-6 text-primary-background capitalize  shadow-[inset_1px_1px_8px_rgba(255,199,225,0.3)] dark:text-primary"
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
