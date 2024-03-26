import Image from 'next/image'
import React from 'react'
import Blossom1 from "../../../public/nfts/blossom1.png";
import Blossom2 from "../../../public/nfts/blossom2.png";
import Blossom3 from "../../../public/nfts/blossom3.png";
import Blossom4 from "../../../public/nfts/blossom4.png";
import Bridge from "../../../public/nfts/bridge.png";
import Wisdom1 from "../../../public/nfts/wisdom1.png";
import Wisdom2 from "../../../public/nfts/wisdom2.png";
import Wisdom3 from "../../../public/nfts/wisdom3.png";
import Wisdom4 from "../../../public/nfts/wisdom4.png";
import Glowing1 from "../../../public/nfts/glowing1.png";
import Glowing2 from "../../../public/nfts/glowing2.png";
import Glowing3 from "../../../public/nfts/glowing3.png";
import Glowing4 from "../../../public/nfts/glowing4.png";
import { NFTCard } from './NFTCard';

export default function NFTDisplays() {
    return (
        <section className='w-full grid md:grid-cols-3 lg:px-32 md:px-4 lg:gap-10 md:gap-8 gap-10  lg:py-28 md:py-20 py-24 radial-gradient'>

            <NFTCard images={[Blossom1, Blossom2, Blossom3, Blossom4, Bridge]} name={"Blossom Tree"} />

            <NFTCard images={[Wisdom1, Wisdom2, Wisdom3, Wisdom4, Bridge]} name={"Tree of Wisdom"} />

            <NFTCard images={[Glowing1, Glowing2, Glowing3, Glowing4, Bridge]} name={"The Glowing Tree"} />

        </section>
    )
}
