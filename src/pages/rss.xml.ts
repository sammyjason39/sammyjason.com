import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE_URL, SITE_NAME, SITE_TAGLINE } from '../lib/site';

export async function GET(context: { site: URL }) {
  const blog = await getCollection('blog', ({ data }) => !data.draft);
  const sorted = blog.sort(
    (a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime()
  );

  return rss({
    title: `${SITE_NAME} | Blog`,
    description: SITE_TAGLINE,
    site: context.site ?? SITE_URL,
    items: sorted.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.id}/`,
    })),
    customData: `<language>id-ID</language>`,
  });
}