import Image from "next/image";
import Link from "next/link";
import { urlFor } from "@/sanity/lib/image";
import type { PostListItem } from "@/sanity/lib/types";

function formatDate(value: string | null) {
  if (!value) return null;
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date(value));
}

export default function PostCard({ post }: { post: PostListItem }) {
  if (!post.slug) return null;

  const date = formatDate(post.publishedAt);
  const categories = (post.categories || []).filter(Boolean);

  return (
    <Link href={`/blog/${post.slug}`} className="group flex flex-col gap-4">
      <div className="relative h-[240px] overflow-hidden rounded-2xl bg-red-500/10">
        {post.mainImage?.asset?._ref ? (
          <Image
            src={urlFor(post.mainImage).width(800).height(480).url()}
            alt={post.mainImage.alt || post.title || ""}
            fill
            className="object-cover transition duration-300 group-hover:scale-105"
            sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
          />
        ) : null}
      </div>
      <div className="flex flex-col gap-2">
        <p className="text-sm text-muted-foreground">
          {[date, post.authorName].filter(Boolean).join(" · ")}
        </p>
        <h2 className="text-xl font-semibold group-hover:text-bridgeRed">
          {post.title}
        </h2>
        {post.excerpt ? (
          <p className="line-clamp-3 text-sm text-muted-foreground">
            {post.excerpt}
          </p>
        ) : null}
        {categories.length > 0 ? (
          <p className="text-sm text-bridgeRed">{categories.join(", ")}</p>
        ) : null}
      </div>
    </Link>
  );
}
