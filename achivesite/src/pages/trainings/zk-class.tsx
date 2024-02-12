import ZkClassView from "@views/zk-class";
import { TRAINING_CLOSED } from "config/constant";

const ZkClassRegistration = () => {
  return (
    <>
      {!TRAINING_CLOSED.zkclass ? (
        <ZkClassView />
      ) : (
        <h1 className="font-bold text-center dark:text-white20 my-52">
          Registration has closed!!
        </h1>
      )}
    </>
  );
};
export default ZkClassRegistration;
