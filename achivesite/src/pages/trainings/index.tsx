import Image from "next/image";
import Link from "next/link";
import { blurUrl } from "data";
import { COHORT_REGISTRATION_OPENED, TRAINING_CLOSED } from "config/constant";

const Card = ({
  imgUrl = "",
  type = "web2",
  text = "Kickstart your career in software development",
  deadline = "",
  link = "",
}) => {
  return (
    <div className="max-w-sm mx-6 my-3 border rounded-md">
      <Link href={link}>
        <a>
          <Image
            src={imgUrl}
            alt="Profile"
            width={400}
            height={400}
            blurDataURL={blurUrl}
          />
          <button className="w-full py-3 capitalize border rounded-b-sm bg-secondary text-secondary font-base border-x-0 dark:text-primary dark:bg-white dark:border-white">
            <p className="font-semibold text-center">{type} Registration</p>
          </button>
        </a>
      </Link>
      <p className="p-2 text-center dark:text-white20">{text}</p>
      <p className="p-2 text-center border text-red-500 font-bold dark:text-white20">{deadline}</p>
    </div>
  );
};

const trainings = [
  {
    component: (
      <Card
        imgUrl="/web-2.svg"
        type="web2"
        deadline="Registration closes on: December 15th, 2023"
        link="/trainings/web2"
        text="Kickstart your career in software development"
      />
    ),
    id: 0,
    closed: TRAINING_CLOSED.web2,
  },
  {
    component: (
      <Card
        imgUrl="/web-3.svg"
        type="web3"
        deadline="Registration closes on: December 8th, 2023"
        link="/trainings/web3"
        text="Transition from web2 to web3"
      />
    ),
    id: 0,
    closed: TRAINING_CLOSED.web3,
  },
  {
    component: (
      <Card
        imgUrl="/programming.svg"
        type="Specialized Class"
        link="/trainings/special-class"
        text="Kickstart your career in software development"
      />
    ),
    id: 0,
    closed: TRAINING_CLOSED.specialClass,
  },
  {
    component: (
      <Card
        imgUrl="/cartesi.png"
        type="Cartesi  Masterclass"
        deadline="Registration closes on: November 30th, 2023"
        link="/trainings/cartesi"
        text="Cartesi Masterclass training program"
      />
    ),
    id: 0,
    closed: TRAINING_CLOSED.cartesi,
  },
  {
  component: (
    <Card
      imgUrl="/zkclass.jpg"
      type="ZK Class"
      link="/trainings/zk-class"
      text="ZK (zero knowledge) Masterclass Training Program"
    />
  ),
  id: 0,
  closed: TRAINING_CLOSED.zkclass,
},
];
const CohortRegistration = () => {
  return (
    <>
      <div className="p-12">
        <div className="flex flex-wrap justify-center p-3 ">
          {trainings
            .sort((a, b) =>
              a.closed === true ? 1 : b.closed === true ? -1 : 0
            )
            .map((i) => {
              return (
                <div className="relative ">
                  {i.component}
                  <div
                    className={`absolute w-full  h-full top-0 ${
                      i.closed ? "" : "hidden"
                    }`}
                  ></div>
                  <div
                    className={`
                    bg-white
                    p-2
                    rounded-md
                    left-1/2
                    -translate-x-1/2
                    text-2xl absolute top-1/2 -translate-y-1/2 ${
                      i.closed ? "" : "hidden"
                    }`}
                  >
                    Closed
                  </div>
                </div>
              );
            })}
        </div>
      </div>
    </>
  );
};

export default CohortRegistration;
