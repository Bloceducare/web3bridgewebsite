import Image from "next/image";
import Link from "next/link";
import { blurUrl } from "data";

const Card = ({
  imgUrl = "",
  type = "web2",
  text = "Kickstart your career in software development",
}) => {
  return (
    <div className="max-w-sm mx-6 my-3 border rounded-md">
      <Link href={`/cohort-registration/${type}`}>
        <a>
          <Image
            src={imgUrl}
            alt="Profile"
            width={400}
            height={400}
            blurDataURL={blurUrl}
          />
          <button className="w-full py-3 capitalize border rounded-b-sm bg-secondary text-secondary font-base  border-x-0 dark:text-primary dark:bg-white dark:border-white">
            <p className="font-semibold text-center">{type} Registration</p>
          </button>
        </a>
      </Link>
      <p className="text-center p-2 dark:text-white20">{text}</p>
    </div>
  );
};
const CohortRegistration = () => {
  return (
    <>
      <div className="p-12">
        <div className="flex flex-wrap justify-center p-3 ">
        <h1 className="font-bold text-center my-48 dark:text-white20">Registration has closed!!</h1>
          {/* <Card
            imgUrl="/web-2.svg"
            type="web2"
            text="Kickstart your career in software development"
          />
          <Card
            imgUrl="/web-3.svg"
            type="web3"
            text="Transistion from web2 to web3"
          /> */}
        </div>
      </div>
    </>
  );
};

export default CohortRegistration;
