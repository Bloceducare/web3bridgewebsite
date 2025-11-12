import React from 'react';
import CustomSectionProps from "@/types/customSection";
import { TextHoverEffect } from "@/components/ui/text-hover-effect";
import { cn } from '@/lib/utils';

const CustomSection: React.FC<CustomSectionProps> = ({heading, description, children}) => (

  <>
  <div  className={cn(
          "h-[10rem] flex items-center justify-center",
        )}>
      <TextHoverEffect text={heading.toUpperCase()}  />
    </div>

    <p className="text-2xl w-[600px] text-center bg-gradient-to-b text-transparent bg-clip-text from-[hsla(40,100%,98%,1)] to-[hsla(40,100%,98%,0.67)]">{description}</p>
    
      {children}
    

  </>

  

)

export default CustomSection;
