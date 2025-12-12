"use client";

import React from "react";
import { Globe, TrendingUp, Users } from "lucide-react";
import { motion } from "framer-motion";
import EthereumLogo from "./EthereumLogo";

export default function PioneerSection() {
  return (
    <section className="py-12 md:py-16 w-full relative bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-10"
        >
          <div className="inline-flex items-center gap-2 mb-6">
            <EthereumLogo size={32} animated={false} />
            <span className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              Pioneering Web3 in Africa
            </span>
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold mb-4 tracking-tight">
            <span className="text-foreground">The First & Only</span>
            <br />
            <span className="bg-gradient-to-r from-bridgeRed to-red-600 bg-clip-text text-transparent">
              Ethereum Hub in Africa
            </span>
          </h2>

          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Establishing Africa&apos;s premier Ethereum community space, fostering innovation 
            and collaboration in decentralized technology.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              icon: Globe,
              title: "First in Africa",
              description: "The pioneering Ethereum community hub on the African continent, setting the standard for Web3 innovation and collaboration.",
              stat: "1st",
            },
            {
              icon: TrendingUp,
              title: "Leading Innovation",
              description: "At the forefront of blockchain development, fostering the next generation of Ethereum builders and researchers.",
              stat: "500+",
            },
            {
              icon: Users,
              title: "Community Driven",
              description: "Built by the community, for the community. A space where African Web3 talent thrives and connects.",
              stat: "50+",
            },
          ].map((item, index) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="p-6 rounded-lg bg-background border border-border hover:border-bridgeRed/30 transition-all group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="w-12 h-12 rounded-lg bg-bridgeRed/10 flex items-center justify-center group-hover:bg-bridgeRed/20 transition-colors">
                    <Icon className="w-6 h-6 text-bridgeRed" />
                  </div>
                  <div className="text-3xl font-bold text-bridgeRed">{item.stat}</div>
                </div>
                <h3 className="text-xl font-semibold mb-3">{item.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{item.description}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
