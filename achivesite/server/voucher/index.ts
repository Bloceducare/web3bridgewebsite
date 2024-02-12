import { userEmail } from "@server/config";
import { sendEmail } from "@server/mailer";
import vouchersDb from "../models/vouchers";

interface IUserDetails {
  userDb: any;
  currentTrack: string;
  name: string;
}

interface IVoucher {
  identifier: string;
  email: string;
  userDetails: IUserDetails;
}

const useVoucher = async ({ identifier, email, userDetails }: IVoucher) => {
  const voucher = await vouchersDb.findOne({
    identifier: identifier.toLowerCase(),
  });

  if (!voucher) {
    throw `${identifier} - invalid voucher`;
  }

  if (voucher.used) {
    throw `${identifier} - voucher used by ${voucher?.user}`;
  }

  try {
    const emailSend = sendEmail({
      email,
      name: userDetails.name,
      type: userDetails.currentTrack,
      currentTrack: userDetails.currentTrack,
      file: userEmail?.[userDetails?.currentTrack],
      userDb: userDetails.userDb,
    });
    const updateVoucher = vouchersDb.updateOne(
      { identifier },
      { $set: { valid: false, user: email, used: true } }
    );

    const [updated] = await Promise.all([emailSend, updateVoucher]);

    return {
      status: true,
      code: 201,
      message: `${identifier} voucher applied successfully`,
      data: updated,
    };
  } catch (e: any) {
    return {
      status: false,
      message: e,
    };
  }
};

export default useVoucher;
