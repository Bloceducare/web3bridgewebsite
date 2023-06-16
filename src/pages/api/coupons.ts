import type { NextApiRequest, NextApiResponse } from "next";
import { createRouter } from "next-connect";
import connectDB, { closeDB } from "@server/config/database";
import vouchersDb from "@server/models/vouchers";
import reportError from "@server/services/report-error";
import genVoucher from "utils/genVoucher";
import { validateCoupon } from "@server/validate";
import { couponSchema } from "schema";

const router = createRouter<NextApiRequest, NextApiResponse>();

router
  .use(async (req, res, next) => {
    await connectDB();

    return next();
  })

  //coupons
  .get(async (req, res) => {
    const { status } = req.query;

    try {
      // const coupons = await  vouchersDb.find({
      //     ...(status=='valid' && {valid:true})
      // })
      const v = await vouchersDb.find();

      // await closeDB()
      // return res.status(200).json({
      //   status: true,
      //   number:coupons.length,
      //       data:coupons,
      //    })
      return res.status(200).json({ data: v });
    } catch (e) {
      return res.status(500).json({
        status: false,
        message: "server error",
      });
    }
  })

  // vouchers
  .post(async (req, res) => {
    const { number } = req.query;

    if (typeof Number(number) != "number") {
      return res.status(423).json({
        status: false,
        message: "invalid coupons number",
      });
    }

    try {
      let coupon:String[] =[];
      coupon = genVoucher(Number(number));
      await Promise.all(
        coupon.map(async (coup) => {
          await new vouchersDb({
            valid: true,
            identifier: coup,
          }).save();
        })
      );

      await closeDB()
      return res.status(200).json({
        status: true,
        data: coupon,
        length: coupon.length,
      });

      // return res.status(200).json({
      //   status: true,
      //   message: "empty generated",
      // });
    } catch (e) {}
  })

  // .delete(async (req, res) => {
  //   const { identifier } = req.query;

  //   try {
  //     // const data = await useCoupon({identifier, email})
  //     //     res.status(201).json(data)
  //     const deleted = await vouchersDb.deleteOne({ identifier})
  //     res.status(201).json({data:deleted});
  //   } catch (e) {
  //     res.status(500).json(e);
  //   }
  // })
  .use(async (req, res, next) => {
    await validateCoupon(couponSchema)(req, res, next);
  })
  .put(async (req, res) => {
    const { identifier, email } = req.query;

    try {
      // const data = await useCoupon({identifier, email})
      //     res.status(201).json(data)
      res.status(201).json({});
    } catch (e) {
      res.status(500).json(e);
    }
  });

export default router.handler({
  // @ts-ignore
  onError: (err, req, res, next) => {
    console.error(err.stack);
    reportError(err);
    res.status(500).end("Something broke!");
  },
  onNoMatch: (req, res) => {
    res.status(404).end("Page is not found info");
  },
});
