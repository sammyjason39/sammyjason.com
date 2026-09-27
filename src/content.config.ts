import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Skema sesuai PRD SAM-71 section 5.1.
// Catatan: Astro 7 memindahkan lokasi config ke src/content.config.ts dan
// mewajibkan loader eksplisit (glob). Bentuk skema tetap identik dengan PRD.
const blogCollection = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string().max(120),
    description: z.string().min(50).max(200),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: z.enum(['catatan-cto', 'framework-4m', 'build-logs', 'refleksi-karir']),
    tags: z.array(z.string()).default([]),
    canonicalUrl: z.string().url().optional(),
    heroImage: z.string().optional(),
    draft: z.boolean().default(false),
    leadAsset: z
      .object({
        keyword: z.string(),
        title: z.string(),
        downloadUrl: z.string(),
      })
      .optional(),
  }),
});

export const collections = {
  blog: blogCollection,
};