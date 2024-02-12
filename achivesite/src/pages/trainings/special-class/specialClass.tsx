import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import SpecialClassView from "@views/specialized/components/form";

import { COHORT_REGISTRATION_OPENED } from "config/constant";
import getTrack from "utils/getTracks";
import { getTotalLeft } from "@views/api";

const Form = () => {
  const { query = {}, asPath } = useRouter();
  const [track, typeOfTrack] = getTrack(asPath);

  const [regStatus, setRegStatus] = useState({
    left: null,
    isCompleted: false,
  });

  useEffect(() => {
    getTotalLeft(track, typeOfTrack).then((res) => setRegStatus(res));
  }, [track, typeOfTrack]);

  return (
    <>
      {COHORT_REGISTRATION_OPENED ? (
        <div>
          {!!regStatus?.left ? (
            <>
            {/* <div className=" max-w-lg m-12 mx-auto dark:text-white20 px-4 text-center text-xl font-semibold">
              <div className=" bg-red-500 p-4  rounded-md">
                {regStatus?.left} Registrations left to Close
              </div>
            </div> */}
            </>
          ) : regStatus?.isCompleted ? (
            <div className="max-w-lg m-12 mx-auto  dark:text-white20 px-4 text-center text-xl font-semibold ">
              <div className=" bg-red-500 p-4  rounded-md">
                Registrations Completed
              </div>
            </div>
          ) : null}

          {!regStatus?.isCompleted ? <SpecialClassView /> : null}
        </div>
      ) : (
        <h1 className="font-bold text-center dark:text-white20 my-52">
          Registration has closed!!
        </h1>
      )}
    </>
  );
};
export default Form;
