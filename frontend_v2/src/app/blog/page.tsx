import type { Metadata } from "next";
import PostCard from "@/components/blog/PostCard";
import MaxWrapper from "@/components/shared/MaxWrapper";
import { client, sanityFetchOptions } from "@/sanity/lib/client";
import { POSTS_QUERY } from "@/sanity/lib/queries";
import type { PostListItem } from "@/sanity/lib/types";

export const metadata: Metadata = {
  title: "Blog | Web3Bridge",
  description: "Stories, updates, and writing from Web3Bridge.",
};

export default async function BlogPage() {
  const posts = await client.fetch<PostListItem[]>(
    POSTS_QUERY,
    {},
    sanityFetchOptions,
  );

  return (
    <MaxWrapper className="py-16">
      <p className="font-medium text-bridgeRed">Journal</p>
      <h1 className="mt-2 text-4xl font-semibold md:text-5xl">Blog</h1>
      <p className="mt-4 max-w-2xl text-muted-foreground">
        Stories and updates from the Web3Bridge community.
      </p>

      {posts.length === 0 ? (
        <p className="mt-12 text-muted-foreground">
          Posts will show up here after they are published in Sanity Studio.
        </p>
      ) : (
        <div className="mt-12 grid gap-10 md:grid-cols-2 lg:grid-cols-3">
          {posts.map((post) => (
            <PostCard key={post._id} post={post} />
          ))}
        </div>
      )}
    </MaxWrapper>
  );
}
