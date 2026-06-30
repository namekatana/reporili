// @ts-check
import { defineConfig } from 'astro/config';

import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

const siteUrl = process.env.PUBLIC_SITE_URL ?? 'https://reporili.tech';

// https://astro.build/config
export default defineConfig({
  site: siteUrl,
  integrations: [svelte(), sitemap()],
  output: 'static',

  vite: {
    plugins: [tailwindcss()],
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
        '/health': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
      },
    },
  },
});