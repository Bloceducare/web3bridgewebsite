"use client";

import React from "react";
import { Target, Heart, Rocket, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const infoSections = [
  {
    icon: Target,
    title: "Our Mission",
    description: "To create a thriving ecosystem where Ethereum builders can collaborate, learn, and innovate together. We&apos;re building a space that fosters creativity and supports the growth of the decentralized web.",
    color: "text-bridgeRed",
  },
  {
    icon: Heart,
    title: "Community First",
    description: "We believe in the power of community. The hub is more than just a workspace—it&apos;s a gathering place for passionate individuals who are shaping the future of blockchain technology.",
    color: "text-red-600",
  },
  {
    icon: Rocket,
    title: "Build the Future",
    description: "Whether you&apos;re building dApps, researching new protocols, or starting a Web3 company, the hub provides the resources and community support you need to succeed.",
    color: "text-orange-500",
  },
];

export default function InfoSection() {
  return (
    <section className="py-12 md:py-16 w-full bg-background">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4 tracking-tight">
            About the Hub
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Africa&apos;s first and only dedicated Ethereum community space, located in the heart of Lagos
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {infoSections.map((section, index) => {
            const Icon = section.icon;
            return (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="p-6 rounded-lg bg-muted/30 border border-border hover:border-bridgeRed/30 transition-all"
              >
                <Icon className={`w-10 h-10 ${section.color} mb-4`} />
                <h3 className="text-xl font-semibold mb-3">{section.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {section.description}
                </p>
              </motion.div>
            );
          })}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-center"
        >
          <div className="inline-block p-8 rounded-lg bg-muted/50 border border-bridgeRed/20">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Join the Community?
            </h3>
            <p className="text-muted-foreground mb-6 max-w-2xl">
              Register now to become part of the Lagos Ethereum Community Hub. 
              Help us manage the space effectively and ensure a productive 
              environment for everyone.
            </p>
            <Link href="/hub/register">
              <Button
                size="lg"
                className="rounded-md px-8 py-6 text-base font-semibold bg-bridgeRed hover:bg-red-600 text-white shadow-lg transition-all"
              >
                Register Now
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

