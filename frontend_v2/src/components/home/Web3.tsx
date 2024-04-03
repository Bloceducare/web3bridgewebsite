import SVGWrapper from "./SVGWrapper"
import img1 from "../../../public/home/Crypto Wallet.png"
import img2 from "../../../public/home/ethereum.png"
import img3 from "../../../public/home/solidity.png"
import img4 from "../../../public/home/foundry.png"
import img5 from "../../../public/home/etherjs.png"
import img6 from "../../../public/home/hardhat.png"
import img7 from "../../../public/home/foundry1.png"
import img8 from "../../../public/home/zk.png"
import img9 from "../../../public/home/hardhat1.png"
import Cards from "./Cards"

const images = [img1, img2, img3, img4, img5, img6, img7, img8, img9];


const Web3 = () => {
    return (
        <section className="w-full flex flex-col items-center md:gap-8 gap-8 justify-center radial-gradient lg:px-6 md:px-2 my-40">
            <div className="flex flex-col items-center gap-3 ">
                <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">The Web 3.0 Cohort</h1>
                <p className="w-full md:w-[70%] text-muted-foreground text-center">In <span className="text-bridgeRed">16 weeks,</span> get everything you need to launch your career in Blockchain Development through our trainings that gives you the nitty gritty of experience through practical classes.</p>
            </div>
            <main className="w-full flex flex-col items-center">
                <SVGWrapper images={images} />
                <Cards />
            </main>
        </section>
    )
}

export default Web3