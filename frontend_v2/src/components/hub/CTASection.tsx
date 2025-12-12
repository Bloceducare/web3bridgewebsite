"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { MoveRight, ArrowRight } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";
import MaxWrapper from "@/components/shared/MaxWrapper";

export default function CTASection() {
  return (
    <section className="py-20 md:py-28 w-full bg-muted/30 relative">
      <MaxWrapper>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto text-center"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">
            Ready to Join the Lagos Ethereum Community Hub?
          </h2>
          <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Become part of a vibrant community of builders, developers, and innovators 
            shaping the future of Ethereum in Lagos. Register now to visit our hub and 
            start your journey.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/hub/register">
              <Button
                size="lg"
                className="rounded-md px-8 py-6 text-base font-semibold bg-bridgeRed hover:bg-red-600 text-white shadow-lg transition-all"
              >
                Register to Visit Hub
                <MoveRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
            
            <Button
              size="lg"
              variant="outline"
              className="rounded-full px-8 py-6 text-base font-semibold border-2"
              onClick={() => {
                document.getElementById("location")?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              Learn More
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
          
          <p className="text-sm text-muted-foreground mt-6">
            Questions? Contact us at{" "}
            <a href="mailto:support@web3bridge.com" className="text-bridgeRed hover:underline">
              support@web3bridge.com
            </a>
          </p>
        </motion.div>
      </MaxWrapper>
    </section>
  );
}

