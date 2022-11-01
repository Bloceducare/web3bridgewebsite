
import codes from 'voucher-code-generator'

const genVoucher = (length=5):String[]=>codes.generate({
    length: 6,
    count: length
})


export default genVoucher;