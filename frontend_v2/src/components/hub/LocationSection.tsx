"use client";

import React from "react";
import { MapPin, Clock, Phone, Mail } from "lucide-react";
import { motion } from "framer-motion";

// Hub location coordinates - Actual location
const HUB_LOCATION = {
  lat: 6.6153, // Ikorodu, Lagos coordinates
  lng: 3.5064,
  address: "25 Talabi Ademola St, Ikorodu, 104102, Lagos, Nigeria",
  name: "Lagos Ethereum Community Hub",
  // Google Maps embed URL with actual coordinates
  mapUrl: `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3964.5!2d3.5064!3d6.6153!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x103bfd4c8b8c8c8b%3A0x8c8c8c8c8c8c8c8c!2s25%20Talabi%20Ademola%20St%2C%20Ikorodu%2C%20104102%2C%20Lagos!5e0!3m2!1sen!2sng!4v1234567890!5m2!1sen!2sng`,
};

export default function LocationSection() {
  return (
    <section id="location" className="py-12 md:py-16 w-full bg-background">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Visit Our Hub
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Come and experience the vibrant Ethereum community in Lagos
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Map */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="rounded-xl overflow-hidden border border-border"
          >
            <iframe
              src={HUB_LOCATION.mapUrl}
              width="100%"
              height="450"
              style={{ border: 0 }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              className="w-full"
              title="Lagos Ethereum Community Hub Location"
            />
          </motion.div>

          {/* Location Info */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="flex flex-col gap-6"
          >
            <div className="p-6 rounded-xl bg-muted/50 border border-border">
              <h3 className="text-2xl font-semibold mb-6 flex items-center gap-2">
                <MapPin className="w-6 h-6 text-bridgeRed" />
                Location Details
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <MapPin className="w-5 h-5 text-muted-foreground mt-1 flex-shrink-0" />
                  <div>
                    <p className="font-medium">{HUB_LOCATION.name}</p>
                    <p className="text-muted-foreground">{HUB_LOCATION.address}</p>
                    <a
                      href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(HUB_LOCATION.address)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-bridgeRed hover:underline text-sm mt-1 inline-block"
                    >
                      Open in Google Maps →
                    </a>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Clock className="w-5 h-5 text-muted-foreground mt-1 flex-shrink-0" />
                  <div>
                    <p className="font-medium">Operating Hours</p>
                    <p className="text-muted-foreground">
                      Monday - Sunday: 24/7 Access<br />
                      (Registered members only)
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Phone className="w-5 h-5 text-muted-foreground mt-1 flex-shrink-0" />
                  <div>
                    <p className="font-medium">Contact</p>
                    <p className="text-muted-foreground">
                      For inquiries, please register through our form
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Mail className="w-5 h-5 text-muted-foreground mt-1 flex-shrink-0" />
                  <div>
                    <p className="font-medium">Email</p>
                    <p className="text-muted-foreground">
                      support@web3bridge.com
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 rounded-xl bg-bridgeRed/10 border border-bridgeRed/20">
              <h4 className="font-semibold mb-2 text-bridgeRed">
                How to Access
              </h4>
              <p className="text-sm text-muted-foreground">
                To visit the hub, please complete the registration form. 
                Once approved, you&apos;ll receive access details and guidelines 
                for using the space.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

