import Image from "next/image"
import UserImage from "../../../public/home/john.png";


const TestimonialCard = () => {
    return (
        <main className="lg:px-44 md:px-10 px-2">
            <div className="w-full flex flex-col items-center gap-4 p-6 border-2 border-bridgeRed/20 bg-brdigeRed/10 rounded-xl">
                <h1 className="text-center font-semibold text-2xl">&quot;The best Cohort Experience&quot;</h1>
                <p className="text-center font-light">It is an awesome program that makes one to focus on learning industry standard Blockchain Development, Without having to worry about basic amenities. I had an awesome experience during the cohort V.</p>
                <div className="flex items-center justify-center gap-2">
                    <Image src={UserImage} alt="UserImage" className="w-12 h-12 rounded-full" />
                    <h4 className="font-medium">John Odey</h4>
                </div>
                <h3 className=" font-light">Blockchain Developer, Lagos.</h3>
            </div>
        </main>
    )
}

export default TestimonialCard