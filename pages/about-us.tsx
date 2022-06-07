import Nav from "../components/Nav";
import Background from "../components/Background";
import HeaderImg from "../assests/about-header-image.svg";
import GroupImg from "../assests/group-image.svg";
import Image from "next/image";
import Button from "../components/Button";
import Footer from "../components/Footer";
type Props = {};

const About = (props: Props) => {
  return (
    <Background>
      <Nav />
      <header className="flex w-[80%] items-center justify-around  mt-12 mx-auto">
        <Image src={HeaderImg} height={326} width={326} />
        <div className="w-[50%]">
          <h1 className="text-[2rem] font-bold mb-6 text-[#151515] dark:text-[#D0D0D0]">
            Hey! I'm Ayodeji, business developer, Blockchain Educator and
            founder of Web 3 bridge.
          </h1>
          <p className="text-[#737373]">
            {" "}
            If you've got a couple of minutes I'd love to share the story of how
            web 3 bridge has grown as a bootstrapped startup. It's been an
            awesome journey and I couldn't have done it without the support of
            my team around me.
          </p>
        </div>
      </header>
      <section className="flex mt-24 mb-12 items-start justify-around  px-8 ">
        <div className="bg-[#F3F3F3] dark:bg-[#111111] px-14 py-12 dark:border dark:border-[#444444]">
          <h1 className="text-center dark:text-white border-b border-b-[#A0A0A0] pb-6 px-4">
            OUR STORY IN TO THE WEB 3
          </h1>
          <ul className="text-[#707070] dark:text-[#D0D0D0] text-sm">
            <li className="my-3">
              <p>Problem</p>
            </li>
            <li className="my-3">
              <p>Solution</p>
            </li>
            <li className="my-3">
              <p>Remote developers</p>
            </li>
            <li className="my-3">
              <p>Lagos</p>
            </li>
            <li className="my-3">
              <p>Physical</p>
            </li>
          </ul>
          <Button
            class="text-center block mx-auto w-full py-2 mt-4"
            type="background"
            content="View Cohorts"
          />
        </div>
        <div className="w-[50%]">
          <Image src={GroupImg} className={"w-full"} />
          <h1 className="mb-6 mt-4 font-bold text-2xl text-[#151515] dark:text-[#D0D0D0]">
            Developers dont have to pay so much to learn web 3
          </h1>
          <p className="mb-4 text-[#737373] dark:text-[#D0D0D0]">
            Web3bridge is a program created in 2019 to train Web3 developers in
            Africa. We are working on building sustainable Web3 economy in
            Africa through remote and onsite Web3 development training,
            supporting web3 developers and startups, and lowering barriers of
            entry into the Web3 ecosystem. 
          </p>
          <p className="mt-6 text-[#737373] dark:text-[#D0D0D0]">
          And we take care of Accomodation
            Feeding and data expenses for all our onsite participants during the
            program to make it easier for them to learn
          </p>
        </div>
      </section>
      <Footer />
    </Background>
  );
};

export default About;
