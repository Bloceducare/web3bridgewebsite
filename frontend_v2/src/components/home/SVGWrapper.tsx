import Image, { StaticImageData } from "next/image"
import SVGLine from "./SVGLine"

const SVGWrapper = ({ images, data }: { images: StaticImageData[], data: { title: string, text: string, img: StaticImageData }[] }) => {
    return (
        <div className="w-[90%] h-[550px] lg:block hidden relative">
            <SVGLine />

            {/* images */}

            <div className="absolute top-4 left-[100px]  flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[0]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Blockchain Security</h4>
            </div>

            <div className="absolute top-4 left-[470px]  flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[1]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Ethereum</h4>
            </div>

            <div className="absolute top-4 right-[100px]  flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[2]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Solidity</h4>
            </div>

            <div className="absolute top-[240px] left-[100px]  flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[3]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Foundry</h4>
            </div>

            <div className="absolute top-[240px] left-[470px]  flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[4]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">EthersJs & Web3Js</h4>
            </div>

            <div className="absolute top-[240px] right-[100px]  flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[5]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Hardhat</h4>
            </div>

            <div className="absolute top-[470px] left-[100px]  flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[6]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Foundry</h4>
            </div>

            <div className="absolute top-[470px] left-[470px] flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[7]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Zero Knowledge</h4>
            </div>

            <div className="absolute top-[470px] right-[100px] flex flex-col items-center">
                <div className="w-[120px] h-[120px]">
                    <Image src={images[8]} alt="Techs" className="w-full h-full" />
                </div>
                <h4 className="font-light text-base">Hardhat</h4>
            </div>
        </div>
    )
}

export default SVGWrapper