"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";

const ParallaxCarousel = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const ringRef = useRef<HTMLDivElement>(null);
  const imgRefs = useRef<HTMLDivElement[]>([]);
  const xPosRef = useRef(0);
  const isDraggingRef = useRef(false);

  const getBgPos = (index: number): string => {
    if (!ringRef.current) return "0px 0px";
    const rotation = gsap.getProperty(ringRef.current, "rotationY") as number;
    const pos =
      100 - (gsap.utils.wrap(0, 360, rotation - 180 - index * 36) / 360) * 500;
    return `${pos}px 0px`;
  };

  const drag = (e: MouseEvent | TouchEvent) => {
    if (!isDraggingRef.current) return;

    const clientX = "touches" in e ? e.touches[0].clientX : e.clientX;

    if (ringRef.current) {
      gsap.to(ringRef.current, {
        rotationY: "-=" + ((Math.round(clientX) - xPosRef.current) % 360),
        onUpdate: () => {
          imgRefs.current.forEach((img, i) => {
            if (img) {
              img.style.backgroundPosition = getBgPos(i);
            }
          });
        },
      });
    }

    xPosRef.current = Math.round(clientX);
  };

  const dragEnd = () => {
    isDraggingRef.current = false;
    if (ringRef.current) {
      gsap.set(ringRef.current, { cursor: "grab" });
    }
  };

  const dragStart = (e: MouseEvent | TouchEvent) => {
    const clientX = "touches" in e ? e.touches[0].clientX : e.clientX;
    xPosRef.current = Math.round(clientX);
    isDraggingRef.current = true;

    if (ringRef.current) {
      gsap.set(ringRef.current, { cursor: "grabbing" });
    }
  };

  useEffect(() => {
    if (!ringRef.current || !containerRef.current) return;

    const timeline = gsap.timeline();

    timeline
      .set(ringRef.current, { rotationY: 180, cursor: "grab" })
      .set(imgRefs.current, {
        rotateY: (i: number) => i * -36,
        transformOrigin: "50% 50% 500px",
        z: -500,
        backgroundImage: (i: number) => `url/public/home/user-${i}.jpg)`,
        backgroundPosition: (i: number) => getBgPos(i),
        backfaceVisibility: "hidden",
        width: "100%",
      })
      .from(imgRefs.current, {
        duration: 1.5,
        y: 200,
        opacity: 0,
        stagger: 0.1,
        ease: "expo",
      })
      .add(() => {
        imgRefs.current.forEach((img) => {
          if (img) {
            img.addEventListener("mouseenter", (e) => {
              gsap.to(imgRefs.current, {
                opacity: (i: number, target: HTMLDivElement) =>
                  target === e.currentTarget ? 1 : 0.5,
                ease: "power3",
              });
            });

            img.addEventListener("mouseleave", () => {
              gsap.to(imgRefs.current, { opacity: 1, ease: "power2.inOut" });
            });
          }
        });
      }, "-=0.5");

    const container = containerRef.current;
    container.addEventListener("mousedown", dragStart);
    container.addEventListener("touchstart", dragStart);
    window.addEventListener("mousemove", drag);
    window.addEventListener("touchmove", drag);
    window.addEventListener("mouseup", dragEnd);
    window.addEventListener("touchend", dragEnd);

    return () => {
      timeline.kill();
      container.removeEventListener("mousedown", dragStart);
      container.removeEventListener("touchstart", dragStart);
      window.removeEventListener("mousemove", drag);
      window.removeEventListener("touchmove", drag);
      window.removeEventListener("mouseup", dragEnd);
      window.removeEventListener("touchend", dragEnd);
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="relative w-[284px] h-[324px] mx-auto"
      style={{ perspective: "2000px" }}
    >
      <div
        ref={ringRef}
        className="absolute w-full h-full"
        style={{ transformStyle: "preserve-3d" }}
      >
        {Array.from({ length: 10 }).map((_, i) => (
          <div
            key={i}
            ref={(el) => {
              if (el) imgRefs.current[i] = el;
            }}
            className="absolute w-full h-full select-none cursor-grab active:cursor-grabbing"
            style={{ transformStyle: "preserve-3d" }}
          />
        ))}
      </div>
    </div>
  );
};

export default ParallaxCarousel;
