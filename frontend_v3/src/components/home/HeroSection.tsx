"use client";
import { buttonVariants } from "../ui/button";
import Link from "next/link";
import { useRouter } from "next/navigation";
import MaxWrapper from "../shared/MaxWrapper";
import { BackgroundLines } from "../ui/background-lines";

const HeroSection = () => {
  const router = useRouter();

  return (
    <section className="flex items-center justify-center lg:h-[95dvh] md:h-[50vh] h-[80vh]  w-full relative overflow-hidden  bg-hero-bg bg-cover bg-center">
      <MaxWrapper className="flex flex-col w-full">
        <main className="w-full h-full absolute top-0 left-0 flex items-center justify-center ">

          <BackgroundLines className="lg:w-[55%] md:w-[60%] w-full flex flex-col md:gap-4 gap-6 items-center justify-center">
            <h1 className="font-semibold lg:text-[56px] md:text-3xl text-[1.72rem] text-center dark:to-white lg:text-7xl relative z-20 animated-heading  ">
              Bridging Developers to the <br /> Blockchain Economy
            </h1>
            <p className="lg:w-[60%] px-8 w-full text-muted-foreground text-center relative z-20">
              Web3Bridge is training Africa’s next generation of blockchain builders Learn. Build. Thrive. From zero to dev in a decentralized world.          </p>
            <div className="flex gap-6 items-center relative z-20">

              <Link
                href={"/more"}
                className={buttonVariants({
                  variant: "bridgeOutline"
                })}

              >
                Learn More
              </Link>
              <Link
                href={"/register"}
                className={buttonVariants({
                  variant: "bridgePrimary",
                })}
              >
                Join the next cohort
              </Link>

            </div>
            {/* <Link
            href="https://docs.google.com/forms/d/e/1FAIpQLScoch9kMWh4ZxkfJyl8IHTrXMGnJWwOjdk3HNpMApkXFEFP3g/viewform"
            target="_blank"
            rel="noreferrer"
            className="rounded-full flex items-center px-12 py-3.5 border-2 ring-2 ring-red-300 dark:ring-red-500 border-red-500 dark:border-red-300 bg-red-500/10 text-bridgeRed text-sm md:text-base capitalize hover:bg-bridgeRed dark:bg-bridgeRed dark:text-red-100 hover:text-red-100">
            Join the next cohort <MoveRight className="w-5 h-5 ml-2 " />
          </Link> */}
          </BackgroundLines>

        </main>
      </MaxWrapper>
    </section>
  );
};

export default HeroSection;
