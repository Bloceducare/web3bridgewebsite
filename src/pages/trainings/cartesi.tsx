import MasterclassView from "@views/cartesi";
import { TRAINING_CLOSED } from "config/constant";

const CairoRegistration = () => {
  return (
    <>
      {!TRAINING_CLOSED.cartesi ? (
        <MasterclassView />
      ) : (
        <h1 className="font-bold text-center dark:text-white20 my-52">
          Registration has closed!!
        </h1>
      )}
    </>
  );
};
export default CairoRegistration;
