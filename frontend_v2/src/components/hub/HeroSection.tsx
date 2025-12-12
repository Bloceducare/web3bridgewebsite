"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { MoveRight, MapPin, ArrowDown } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";
import dynamic from "next/dynamic";
import EthereumLogo from "./EthereumLogo";

// Dynamically import Vanta.js to avoid SSR issues
const VantaWaves = dynamic(() => import("@/components/hub/VantaBackground"), {
  ssr: false,
});

export default function HeroSection() {
  return (
    <section className="flex flex-col items-center justify-center min-h-[90vh] w-full relative overflow-hidden">
      {/* Vanta.js Animated Background - subtle */}
      <VantaWaves />
      
      {/* Professional gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background/95 to-background z-10" />
      
      {/* Subtle grid pattern */}
      <div className="absolute inset-0 opacity-[0.02] z-5" style={{
        backgroundImage: `linear-gradient(rgba(250, 1, 1, 0.1) 1px, transparent 1px),
                         linear-gradient(90deg, rgba(250, 1, 1, 0.1) 1px, transparent 1px)`,
        backgroundSize: '50px 50px',
      }} />

      <div className="relative z-20 w-full max-w-6xl mx-auto px-4 md:px-6 flex flex-col items-center gap-12 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="flex flex-col items-center gap-8"
        >
          {/* Professional badge */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="inline-flex items-center gap-3 px-4 py-2 rounded-md bg-bridgeRed/5 border border-bridgeRed/20 backdrop-blur-sm"
          >
            <EthereumLogo size={18} animated={false} />
            <span className="text-sm font-medium text-muted-foreground">
              First Ethereum Community Hub in Africa
            </span>
          </motion.div>
          
          {/* Main title - clean and professional */}
          <div className="space-y-4">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="font-bold leading-tight text-5xl md:text-6xl lg:text-7xl tracking-tight"
            >
              <span className="text-foreground">Lagos Ethereum</span>
              <br />
              <span className="bg-gradient-to-r from-bridgeRed to-red-600 bg-clip-text text-transparent">
                Community Hub
              </span>
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed font-light"
            >
              A dedicated space for builders, researchers, and innovators in the Ethereum ecosystem. 
              Supporting the growth of decentralized technology across Africa.
            </motion.p>
          </div>
          
          {/* CTA buttons - professional */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="flex flex-col sm:flex-row items-center gap-4 mt-4"
          >
            <Link href="/hub/register">
              <Button
                size="lg"
                className="rounded-md px-8 py-6 text-base font-semibold bg-bridgeRed hover:bg-red-600 text-white shadow-lg hover:shadow-xl transition-all"
              >
                Register to Visit
                <MoveRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
            
            <Button
              size="lg"
              variant="outline"
              className="rounded-md px-8 py-6 text-base font-semibold border-2 hover:bg-muted transition-all"
              onClick={() => {
                document.getElementById("location")?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              <MapPin className="w-5 h-5 mr-2" />
              View Location
            </Button>
          </motion.div>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="flex flex-col items-center gap-2 text-muted-foreground"
          >
            <span className="text-xs font-medium">Scroll to explore</span>
            <ArrowDown className="w-5 h-5" />
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
