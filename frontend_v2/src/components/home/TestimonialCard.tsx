import Image from "next/image"
import React from "react";
import testimonialProps from "@/types/testimonialCard";



const TestimonialCard: React.FC<testimonialProps> = ({ title, description, user, role,image }) => {
    return (
        <main className="lg:px-44 md:px-10 px-2">
            <div className="w-full flex flex-col items-center gap-4 p-6 border-2 border-bridgeRed/20 dark:border-bridgeRed/40 bg-brdigeRed/10 rounded-xl">
                <h1 className="text-center font-semibold text-2xl">&quot;{title}&quot;</h1>
                <p className="text-center font-light">{description}</p>
                <div className="flex items-center justify-center gap-2">
                    <Image src={image || ""} alt="UserImage" className="w-12 h-12 rounded-full" width={12} height={12} />
                    <h4 className="font-medium">{user}</h4>
                </div>
                <h3 className=" font-light">{role}</h3>
            </div>
        </main>
    )
}

export default TestimonialCard