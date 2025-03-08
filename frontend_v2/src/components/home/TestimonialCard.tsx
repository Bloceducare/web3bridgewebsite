import Image from "next/image";
import React, { useState } from "react";
import testimonialProps from "@/types/testimonialCard";

const TestimonialCard: React.FC<testimonialProps> = ({
  title,
  description,
  user,
  role,
  image,
}) => {
  const [showFullDescription, setShowFullDescription] = useState(false);
  const toggleDescription = () => setShowFullDescription(!showFullDescription);

  const truncatedDescription =
    description.length > 500 ? description.slice(0, 500) + "..." : description;

  return (
    <main className="lg:px-44 md:px-10 px-2">
      <div className="w-full flex flex-col items-center gap-4 p-6 border-2 border-bridgeRed/20 dark:border-bridgeRed/40 bg-brdigeRed/10 rounded-xl">
        <p className="text-center transition-all duration-300 font-light">
          {showFullDescription ? description : truncatedDescription}
        </p>
        {description.length > 500 && (
          <button onClick={toggleDescription} className="text-bridgeRed">
            {showFullDescription ? "Show less" : "Show more"}
          </button>
        )}
        <div className="flex items-center justify-center gap-2">
          <Image
            src={image || ""}
            alt="UserImage"
            className="w-12 h-12 rounded-full"
            width={12}
            height={12}
          />
          <h4 className="font-medium">{user}</h4>
        </div>
      </div>
    </main>
  );
};

export default TestimonialCard;
