// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import remarkGithubBlockquoteAlert from 'remark-github-blockquote-alert';

const SITE = 'https://sammyjason.com';

// https://astro.build/config
export default defineConfig({
  site: SITE,
  output: 'static',
  trailingSlash: 'never',
  integrations: [mdx(), sitemap()],
  markdown: {
    syntaxHighlight: 'shiki',
    shikiConfig: {
      theme: 'github-dark-default',
      wrap: true,
    },
    remarkPlugins: [[remarkGithubBlockquoteAlert, { style: 'plain' }]],
  },
  vite: {
    plugins: [tailwindcss()],
  },
});