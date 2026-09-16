import { defineConfig } from "astro/config";

// SITE_URL and BASE_PATH let the same build run on a custom domain,
// Read the Docs or a GitHub Pages sub-path.
export default defineConfig({
  site: process.env.SITE_URL ?? "https://telegrinder.rtfd.io",
  base: process.env.BASE_PATH ?? "/",
  trailingSlash: "always",
  compressHTML: true,
  prefetch: { prefetchAll: true, defaultStrategy: "hover" },
  devToolbar: { enabled: false },
  vite: {
    server: { fs: { allow: [".."] } },
  },
});
