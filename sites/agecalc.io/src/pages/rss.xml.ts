import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { siteConfig, siteUrl } from '~/config/site.config';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  if (!siteConfig.features.hasBlog) {
    return new Response('RSS disabled for this site', { status: 404 });
  }
  const posts = (await getCollection('blog', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf(),
  );
  return rss({
    title: siteConfig.identity.name,
    description: siteConfig.identity.description,
    site: context.site ?? siteUrl,
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.description,
      pubDate: p.data.publishDate,
      link: `/blog/${p.slug}/`,
    })),
    customData: `<language>${siteConfig.identity.language}</language>`,
  });
}
