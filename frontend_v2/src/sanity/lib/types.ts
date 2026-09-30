import type { PortableTextBlock } from "next-sanity";

export type SanityImage = {
  alt?: string | null;
  caption?: string | null;
  asset?: {
    _ref?: string;
    _type?: string;
  } | null;
} | null;

export type PostListItem = {
  _id: string;
  title: string | null;
  slug: string | null;
  excerpt: string | null;
  publishedAt: string | null;
  mainImage: SanityImage;
  authorName: string | null;
  categories: Array<string | null> | null;
};

export type Post = {
  _id: string;
  title: string | null;
  slug: string | null;
  excerpt: string | null;
  publishedAt: string | null;
  mainImage: SanityImage;
  body: PortableTextBlock[] | null;
  seo: {
    title?: string | null;
    description?: string | null;
  } | null;
  author: {
    name: string | null;
    slug: string | null;
    image: SanityImage;
    bio: string | null;
  } | null;
  categories: Array<{
    _id: string;
    title: string | null;
    slug: string | null;
  } | null> | null;
};
