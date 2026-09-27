# sammyjason.com

Situs pribadi & blog teknis **Samuel Jason (Samz)**: CTO Conextlab, N8N Ambassador, Founder Belajar AI.

> Teman kamu bertumbuh di Era AI.

Dibangun dengan [Astro](https://astro.build) (static output), Tailwind CSS v4, dan markdown content collections. Tidak ada web font eksternal, tidak ada tracker default, dan tidak ada client JS di luar interaksi kecil (menu mobile, copy code, form kontak).

## Stack

| Bagian | Pilihan |
| :--- | :--- |
| Framework | Astro (static, `output: 'static'`) |
| Styling | Tailwind CSS v4 via `@tailwindcss/vite` + `@tailwindcss/typography` |
| Konten | Content Collections + zod (`src/content.config.ts`) |
| Blog | Markdown (`src/content/blog/*.md`), 4 kategori |
| RSS | `@astrojs/rss` → `/rss.xml` |
| Sitemap | `@astrojs/sitemap` → `/sitemap-index.xml` |
| Form | Web3Forms (`PUBLIC_WEB3FORMS_KEY`) + honeypot + fallback `mailto:` |
| Deploy | Docker multi-stage (node:20-alpine builder + nginx:alpine) |

## Perintah

| Command | Aksi |
| :--- | :--- |
| `npm install` | Pasang dependensi |
| `npm run dev` | Dev server di `localhost:4321` |
| `npm run build` | Build produksi ke `./dist/` |
| `npm run preview` | Preview hasil build |

## Struktur

```text
/
├── public/              # aset statis (favicon, robots.txt, og.png, sam.svg)
├── src/
│   ├── components/      # Avatar, Header, Footer, Seo, dll.
│   ├── content/blog/    # artikel markdown + frontmatter zod
│   ├── layouts/         # BaseLayout (SEO + JSON-LD + shell)
│   ├── lib/site.ts      # konstanta situs, kategori, helper
│   ├── pages/           # / /tentang /karya /kelas /blog /kontak /404
│   └── styles/          # global.css (Tailwind v4 + komponen)
├── Dockerfile           # multi-stage sesuai PRD section 6
└── nginx.conf           # gzip, security headers, cache, try_files
```

## Environment

| Variabel | Default | Fungsi |
| :--- | :--- | :--- |
| `PUBLIC_WEB3FORMS_KEY` | `FORM-KEY-PENDING` | Kunci Web3Forms. Kalau belum disetel, form fallback ke `mailto:` |
| `PUBLIC_GA_ID` | kosong | Opsional. Kalau diset, GA4 termuat (zero tracker default) |

## Avatar

Slot foto asli ada di `public/sam.jpg`. Selama file itu belum ada, komponen `Avatar` otomatis memakai monogram inisial "SJ" (SVG gradien) dari `public/sam.svg`. Begitu foto diunggah dan di-rebuild, foto otomatis dipakai.

## Deploy

Dokploy menarik repo ini, build Dockerfile, dan menyajikan `dist/` via nginx:alpine. Domain target: `sammyjason.com` (SSL via Traefik Let's Encrypt).

---

Dibuat dan dirawat sendiri oleh Samz. © 2026 Samuel Jason Santosa.