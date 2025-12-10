"use client";

import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';

interface CarouselImage {
  id: string;
  description: string;
  imageUrl: string;
  imageHint: string;
}

interface ParallaxCarouselProps {
  images: CarouselImage[];
}

const ParallaxCarousel: React.FC<ParallaxCarouselProps> = ({ images }) => {
  const ringRef = useRef<HTMLDivElement>(null);
  const xPos = useRef(0);
  const imageElementsRef = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    const ring = ringRef.current;
    const imgs = imageElementsRef.current.filter(el => el !== null) as HTMLDivElement[];
    if (!ring || imgs.length === 0) return;

    const numImages = imgs.length;
    const anglePerImage = 360 / numImages;
    const radius = 400; // Reduced radius to bring images closer

    const getBgPos = (i: number): string => {
      const ringRotation = gsap.getProperty(ring, 'rotationY') as number;
      const wrappedRotation = gsap.utils.wrap(0, 360, ringRotation - 180 - i * anglePerImage);
      return `${100 - (wrappedRotation / 360) * radius}px 0px`;
    };

    const tl = gsap.timeline();
    tl.set(ring, { rotationY: 180, cursor: 'grab' })
      .set(imgs, {
        rotateY: (i) => i * -anglePerImage,
        transformOrigin: `50% 50% ${radius}px`,
        z: -radius,
        backgroundImage: (i) => `url(${images[i].imageUrl})`,
        backgroundPosition: (i) => getBgPos(i),
        backfaceVisibility: 'hidden',
      })
      .from(imgs, {
        duration: 1.5,
        y: 200,
        opacity: 0,
        stagger: 0.05, // Reduced stagger for a quicker entry
        ease: 'expo',
      })
      .add(() => {
        imgs.forEach((img) => {
          img.addEventListener('mouseenter', handleMouseEnter);
          img.addEventListener('mouseleave', handleMouseLeave);
        });
      }, '-=0.5');

    const handleMouseEnter = (e: MouseEvent) => {
      const current = e.currentTarget;
      gsap.to(imgs, { opacity: (i, t) => (t === current ? 1 : 0.5), ease: 'power3' });
    };

    const handleMouseLeave = () => {
      gsap.to(imgs, { opacity: 1, ease: 'power2.inOut' });
    };

    const dragStart = (e: MouseEvent | TouchEvent) => {
      const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
      xPos.current = Math.round(clientX);
      gsap.set(ring, { cursor: 'grabbing' });
      window.addEventListener('mousemove', drag);
      window.addEventListener('touchmove', drag, { passive: true });
    };

    const drag = (e: MouseEvent | TouchEvent) => {
      const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
      const newX = Math.round(clientX);
      const delta = newX - xPos.current;

      gsap.to(ring, {
        rotationY: `-=${delta}`,
        onUpdate: () => {
          gsap.set(imgs, { backgroundPosition: (i) => getBgPos(i) });
        },
      });

      xPos.current = newX;
    };

    const dragEnd = () => {
      window.removeEventListener('mousemove', drag);
      window.removeEventListener('touchmove', drag);
      gsap.set(ring, { cursor: 'grab' });
    };

    window.addEventListener('mousedown', dragStart);
    window.addEventListener('touchstart', dragStart, { passive: true });
    window.addEventListener('mouseup', dragEnd);
    window.addEventListener('touchend', dragEnd);

    return () => {
      window.removeEventListener('mousedown', dragStart);
      window.removeEventListener('touchstart', dragStart);
      window.removeEventListener('mouseup', dragEnd);
      window.removeEventListener('touchend', dragEnd);
      window.removeEventListener('mousemove', drag);
      window.removeEventListener('touchmove', drag);

      imgs.forEach((img) => {
        img.removeEventListener('mouseenter', handleMouseEnter);
        img.removeEventListener('mouseleave', handleMouseLeave);
      });

      tl.kill();
      gsap.killTweensOf([ring, ...imgs]);
    };
  }, [images]);

  return (
    <div className="w-full h-full [transform-style:preserve-3d] relative">
      <div className="relative w-[284px] h-[324px] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 [perspective:4000px]">
        <div ref={ringRef} className="absolute w-full h-full [transform-style:preserve-3d] select-none">
          {images.map((image, i) => (
            <div
              key={image.id}
              ref={(el) => { imageElementsRef.current[i] = el }}
              className="img absolute w-full h-full bg-cover bg-no-repeat bg-center  rounded-tl-xl rounded-tr-xl"
              data-ai-hint={image.imageHint}
            ></div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ParallaxCarousel;

