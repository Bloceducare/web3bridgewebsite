import SVGWrapper from "./SVGWrapper";
import img1 from "../../../public/home/Crypto Wallet.png";
import img2 from "../../../public/home/ethereum.png";
import img3 from "../../../public/home/solidity.png";
import img4 from "../../../public/home/foundry.png";
import img5 from "../../../public/home/etherjs.png";
import img6 from "../../../public/home/hardhat.png";
import img7 from "../../../public/home/foundry1.png";
import img8 from "../../../public/home/zk.png";
import img9 from "../../../public/home/hardhat1.png";
import img10 from "../../../public/home/blockchain.png";
import Cards from "./Cards";
import CTA from "./CTA";

const images = [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10];

const Web3 = () => {
  const data = [
    {
      title: "Intro to Blockchain",
      text: "Learn blockchain basics: decentralized networks, consensus, and cryptography for secure systems.",
      img: images[9],
    },
    {
      title: "Ethereum",
      text: "Explore Ethereum, a leading platform for smart contracts and dApps.",
      img: images[1],
    },
    {
      title: "Solidity",
      text: "Learn Solidity for writing smart contracts on Ethereum.",
      img: images[2],
    },
    // {
    //   title: "Foundry",
    //   text: "Get everything you need to launch your career as a smart contract developer",
    //   img: images[3],
    // },
    {
      title: "EtherJS & Web3JS",
      text: "Use EtherJS and Web3JS to interact with Ethereum smart contracts.",
      img: images[4],
    },
    {
      title: "Hardhat",
      text: "Streamline smart contract development with Hardhat.",
      img: images[5],
    },
    {
      title: "Foundry",
      text: "Explore Foundry, an advanced tool for smart contract development.",
      img: images[6],
    },
    {
      title: "Non-Fungible Tokens",
      text: "Understand NFTs, a key application of blockchain technology.",
      img: images[8],
    },
    {
      title: "Zero Knowledge",
      text: "Learn about zero-knowledge proofs for privacy in blockchain.",
      img: images[7],
    },
    {
      title: "Blockchain Security",
      text: "Understand the measures taken to protect blockchain networks, data, and transactions from unauthorized access, fraud, and other malicious activities.",
      img: images[0],
    },
  ];
  return (
    <section className="w-full flex flex-col items-center md:gap-8 gap-8 justify-center radial-gradient lg:px-6 md:px-2 md:my-40 my-32">
      <div className="flex flex-col items-center gap-3 ">
        <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">
          The Web 3.0 Cohort
        </h1>
        <p className="w-full md:w-[70%] text-muted-foreground text-center">
          In <span className="text-bridgeRed">16 weeks,</span> get everything
          you need to launch your career in Blockchain Development through our
          trainings that gives you the nitty gritty of experience through
          practical classes.
        </p>
      </div>
      <main className="w-full flex flex-col items-center">
        <SVGWrapper data={data} />
        <Cards data={data} />
      </main>

      <CTA />
    </section>
  );
};

export default Web3;
