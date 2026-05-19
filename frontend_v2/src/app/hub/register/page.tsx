"use client";

import React from "react";
import MaxWrapper from "@/components/shared/MaxWrapper";
import Link from "next/link";
import { ArrowLeft, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function HubRegistrationPage() {
  return (
    <div className="min-h-[85vh] flex flex-col justify-center bg-gradient-to-b from-background to-muted/20 py-8 md:py-12 relative overflow-hidden">
      {/* Background ambient glow matching the hub's theme */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-bridgeRed/5 rounded-full blur-[100px] pointer-events-none" />

      <MaxWrapper>
        <div className="mb-6 z-10 relative">
          <Link href="/hub">
            <Button variant="ghost" className="mb-4 group text-muted-foreground hover:text-foreground transition-colors">
              <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
              Back to Hub
            </Button>
          </Link>
        </div>
        
        <div className="flex flex-col items-center justify-center w-full min-h-[55vh] z-10 relative">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="w-full max-w-2xl bg-card/45 backdrop-blur-md border border-border/80 rounded-2xl p-8 md:p-12 shadow-2xl relative overflow-hidden text-center flex flex-col items-center gap-6"
          >
            {/* Top theme-accent bar */}
            <div className="absolute top-0 left-0 right-0 h-[4px] bg-gradient-to-r from-bridgeRed via-red-500 to-bridgeRed" />
            
            {/* Sleek, pulsing icon badge */}
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 100 }}
              className="w-16 h-16 rounded-full bg-bridgeRed/10 flex items-center justify-center border border-bridgeRed/20 text-bridgeRed mb-2"
            >
              <ExternalLink className="w-8 h-8 animate-pulse" />
            </motion.div>

            {/* Premium Typography & Content */}
            <div className="space-y-4">
              <motion.h1 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-3xl md:text-4xl font-extrabold tracking-tight text-foreground"
              >
                We have <span className="bg-gradient-to-r from-bridgeRed to-red-500 bg-clip-text text-transparent">Moved!</span>
              </motion.h1>
              
              <motion.p 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="text-lg md:text-xl text-muted-foreground font-light leading-relaxed max-w-lg mx-auto"
              >
                We have moved to a new site. Click on this link to register for the hub:
              </motion.p>
            </div>

            {/* CTA Register Button */}
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="w-full mt-4 flex flex-col items-center gap-4"
            >
              <Link 
                href="https://ethereum.web3bridgeafrica.com/member" 
                target="_blank" 
                rel="noopener noreferrer"
                className="w-full sm:w-auto"
              >
                <Button 
                  size="lg"
                  className="w-full sm:w-auto px-10 py-7 text-base font-bold rounded-xl bg-bridgeRed hover:bg-red-600 text-white shadow-lg hover:shadow-red-500/20 hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200 flex items-center justify-center gap-2"
                >
                  Register for the Hub
                  <ExternalLink className="w-5 h-5" />
                </Button>
              </Link>

              <span className="text-xs text-muted-foreground">
                Redirecting link:{" "}
                <a 
                  href="https://ethereum.web3bridgeafrica.com/member" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-bridgeRed hover:underline transition-all font-medium"
                >
                  ethereum.web3bridgeafrica.com/member
                </a>
              </span>
            </motion.div>
          </motion.div>
        </div>
      </MaxWrapper>
    </div>
  );
}


