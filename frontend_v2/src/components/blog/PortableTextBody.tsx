import { PortableText, type PortableTextComponents } from "next-sanity";
import Image from "next/image";
import { urlFor } from "@/sanity/lib/image";
import type { Post } from "@/sanity/lib/types";

const components: PortableTextComponents = {
  types: {
    image: ({ value }) => {
      if (!value?.asset?._ref) return null;

      return (
        <figure className="my-8">
          <Image
            src={urlFor(value).width(1600).url()}
            alt={value.alt || ""}
            width={1600}
            height={900}
            className="h-auto w-full rounded-2xl"
          />
          {value.caption ? (
            <figcaption className="mt-2 text-sm text-muted-foreground">
              {value.caption}
            </figcaption>
          ) : null}
        </figure>
      );
    },
  },
  block: {
    h2: ({ children }) => (
      <h2 className="mb-4 mt-10 text-3xl font-semibold">{children}</h2>
    ),
    h3: ({ children }) => (
      <h3 className="mb-3 mt-8 text-2xl font-semibold">{children}</h3>
    ),
    h4: ({ children }) => (
      <h4 className="mb-3 mt-6 text-xl font-semibold">{children}</h4>
    ),
    blockquote: ({ children }) => (
      <blockquote className="my-6 border-l-4 border-bridgeRed pl-4 italic">
        {children}
      </blockquote>
    ),
    normal: ({ children }) => (
      <p className="mb-4 text-base leading-7">{children}</p>
    ),
  },
  list: {
    bullet: ({ children }) => (
      <ul className="mb-4 list-disc space-y-2 pl-6">{children}</ul>
    ),
    number: ({ children }) => (
      <ol className="mb-4 list-decimal space-y-2 pl-6">{children}</ol>
    ),
  },
  marks: {
    link: ({ children, value }) => {
      const href = value?.href || "#";
      return (
        <a
          href={href}
          className="text-bridgeRed underline"
          rel="noreferrer"
          target="_blank"
        >
          {children}
        </a>
      );
    },
  },
};

export default function PortableTextBody({
  value,
}: {
  value: Post["body"];
}) {
  if (!value?.length) return null;

  return <PortableText value={value} components={components} />;
}
