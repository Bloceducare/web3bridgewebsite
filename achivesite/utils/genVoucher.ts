
import codes from 'voucher-code-generator'

const genVoucher = (count=5, length=6):String[]=>codes.generate({
    length,
    count,
    charset: "123456789abcdefghijklmnpqwxyz"
})


export default genVoucher;