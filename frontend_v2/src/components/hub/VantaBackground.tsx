"use client";

import { useEffect, useRef } from "react";

export default function VantaBackground() {
  const vantaRef = useRef<HTMLDivElement>(null);
  const vantaEffect = useRef<any>(null);

  useEffect(() => {
    if (!vantaRef.current) return;

    const loadVanta = async () => {
      try {
        // Dynamically import vanta.js
        // @ts-ignore - Vanta types may not be available
        const THREE = await import("three");
        // @ts-ignore - Vanta types may not be available
        const VANTA = await import("vanta/dist/vanta.waves.min.js");

        if (vantaRef.current && !vantaEffect.current) {
          vantaEffect.current = (VANTA as any).default({
            el: vantaRef.current,
            THREE: THREE.default,
            mouseControls: false,
            touchControls: false,
            gyroControls: false,
            minHeight: 200.0,
            minWidth: 200.0,
            scale: 1.0,
            scaleMobile: 1.0,
            color: 0x627eea, // Ethereum purple - subtle
            shininess: 20.0,
            waveHeight: 8.0,
            waveSpeed: 0.5,
            zoom: 0.65,
          });
        }
      } catch (error) {
        console.error("Error loading Vanta.js:", error);
        // Fallback to subtle gradient
        if (vantaRef.current) {
          vantaRef.current.className = "absolute inset-0 bg-gradient-to-br from-bridgeRed/3 via-purple-500/2 to-bridgeRed/3";
        }
      }
    };

    loadVanta();

    return () => {
      if (vantaEffect.current) {
        vantaEffect.current.destroy();
        vantaEffect.current = null;
      }
    };
  }, []);

  return <div ref={vantaRef} className="absolute inset-0 w-full h-full opacity-30" />;
}
