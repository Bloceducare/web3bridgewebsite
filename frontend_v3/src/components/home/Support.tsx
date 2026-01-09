import { ArrowUpRight } from "lucide-react";
import MaxWrapper from "../shared/MaxWrapper";
import { buttonVariants } from "../ui/button";
import Link from "next/link"

export default function Support() {
  return (
    <section className="mb-24">
      <MaxWrapper>
        <div className="text-center ">
          <div className="space-y-2 mb-8">
            <h2 className="text-transparent bg-clip-text bg-gradient-to-b from-[hsl(0,0%,100%)] to-[hsl(0,0%,29%)] text-[2.5rem]">Need clarifications and support?</h2>
            <p className="text-[hsla(227,4%,52%,1)]">Reach out to <span className="text-white font-medium">Support@web3bridge.com</span> for any queries</p>
          </div>
          <Link
            href={"/more"}
            className={buttonVariants({
              variant: "bridgeOutline"
            })}

          >
            Learn About Us <ArrowUpRight />
          </Link>


        </div>
      </MaxWrapper>
    </section>
  )
}

