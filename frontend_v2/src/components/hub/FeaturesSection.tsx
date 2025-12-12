"use client";

import React from "react";
import { Code2, Users, BookOpen, Zap, Network, Shield } from "lucide-react";
import { motion } from "framer-motion";

const features = [
  {
    icon: Code2,
    title: "Development Space",
    description: "Dedicated workspace with high-speed internet, power outlets, and comfortable seating for coding and building.",
  },
  {
    icon: Users,
    title: "Community Events",
    description: "Regular meetups, workshops, hackathons, and networking events to connect with fellow Ethereum builders.",
  },
  {
    icon: BookOpen,
    title: "Learning Resources",
    description: "Access to Ethereum documentation, tutorials, and educational materials to enhance your skills.",
  },
  {
    icon: Zap,
    title: "Innovation Hub",
    description: "A space where ideas come to life. Collaborate on projects, get feedback, and build the next big thing.",
  },
  {
    icon: Network,
    title: "Networking",
    description: "Connect with developers, founders, researchers, and investors in the Ethereum ecosystem.",
  },
  {
    icon: Shield,
    title: "Secure Environment",
    description: "Safe and secure space with proper infrastructure to support your development and research work.",
  },
];

export default function FeaturesSection() {
  return (
    <section className="py-24 md:py-32 w-full bg-background">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4 tracking-tight">
            What We Offer
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Everything you need to build, learn, and grow in the Ethereum ecosystem
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
                className="p-6 rounded-lg bg-muted/30 border border-border hover:border-bridgeRed/30 hover:bg-muted/50 transition-all group"
              >
                <div className="w-12 h-12 rounded-lg bg-bridgeRed/10 flex items-center justify-center mb-4 group-hover:bg-bridgeRed/20 transition-colors">
                  <Icon className="w-6 h-6 text-bridgeRed" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
