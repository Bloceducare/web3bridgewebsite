import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import PortableTextBody from "@/components/blog/PortableTextBody";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { client, sanityFetchOptions } from "@/sanity/lib/client";
import { urlFor } from "@/sanity/lib/image";
import { POST_QUERY, POST_SLUGS_QUERY } from "@/sanity/lib/queries";
import type { Post } from "@/sanity/lib/types";

function formatDate(value: string | null) {
  if (!value) return null;
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date(value));
}

export async function generateStaticParams() {
  const posts = await client
    .withConfig({ useCdn: false })
    .fetch<Array<{ slug: string }>>(POST_SLUGS_QUERY, {}, sanityFetchOptions);

  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const post = await client.fetch<Post | null>(
    POST_QUERY,
    { slug: params.slug },
    sanityFetchOptions,
  );

  if (!post) {
    return { title: "Blog | Web3Bridge" };
  }

  const title = post.seo?.title || post.title || "Blog";
  const description = post.seo?.description || post.excerpt || undefined;
  const image = post.mainImage?.asset?._ref
    ? urlFor(post.mainImage).width(1200).height(630).url()
    : undefined;

  return {
    title: `${title} | Web3Bridge`,
    description,
    openGraph: {
      title,
      description,
      images: image ? [{ url: image }] : undefined,
    },
  };
}

export default async function BlogPostPage({
  params,
}: {
  params: { slug: string };
}) {
  const post = await client.fetch<Post | null>(
    POST_QUERY,
    { slug: params.slug },
    sanityFetchOptions,
  );

  if (!post) notFound();

  const date = formatDate(post.publishedAt);
  const categories = (post.categories || []).filter(
    (category): category is NonNullable<typeof category> => Boolean(category),
  );

  return (
    <MaxWrapper className="py-16">
      <article className="mx-auto max-w-3xl">
        <Link href="/blog" className="text-sm text-bridgeRed">
          Back to blog
        </Link>
        <h1 className="mt-6 text-4xl font-semibold md:text-5xl">{post.title}</h1>
        <p className="mt-4 text-sm text-muted-foreground">
          {[date, post.author?.name].filter(Boolean).join(" · ")}
        </p>
        {categories.length > 0 ? (
          <p className="mt-2 text-sm text-bridgeRed">
            {categories.map((category) => category.title).filter(Boolean).join(", ")}
          </p>
        ) : null}
        {post.mainImage?.asset?._ref ? (
          <div className="relative mt-8 aspect-[16/9] overflow-hidden rounded-2xl">
            <Image
              src={urlFor(post.mainImage).width(1600).height(900).url()}
              alt={post.mainImage.alt || post.title || ""}
              fill
              priority
              className="object-cover"
              sizes="(min-width: 768px) 768px, 100vw"
            />
          </div>
        ) : null}
        <div className="mt-10">
          <PortableTextBody value={post.body} />
        </div>
      </article>
    </MaxWrapper>
  );
}
