export const SITE_URL = 'https://sammyjason.com';
export const SITE_NAME = 'Samuel Jason';
export const SITE_TAGLINE = 'Teman kamu bertumbuh di Era AI.';

export const CATEGORIES: Record<string, { label: string; description: string }> = {
  'catatan-cto': {
    label: 'Catatan CTO',
    description:
      'Arsitektur tingkat tinggi, kepemimpinan teknis, evaluasi model, dan observabilitas produksi.',
  },
  'framework-4m': {
    label: 'Framework 4M',
    description:
      'Panduan adopsi AI bisnis langkah demi langkah untuk founder dan tim operasional.',
  },
  'build-logs': {
    label: 'Build Logs',
    description:
      'Tutorial teknis mendalam, hands-on konfigurasi server, setup Docker, n8n, dan code snippets.',
  },
  'refleksi-karir': {
    label: 'Refleksi & Karir',
    description:
      'Catatan personal, etika AI, perjalanan talenta teknologi, dan kepemimpinan.',
  },
};

export const NAV_LINKS = [
  { href: '/tentang/', label: 'Tentang' },
  { href: '/karya/', label: 'Karya' },
  { href: '/kelas/', label: 'Kelas & Ngobrol' },
  { href: '/blog/', label: 'Blog' },
  { href: '/kontak/', label: 'Kontak' },
];

export const SOCIAL_LINKS = [
  { href: 'https://linkedin.com/in/samueljasonsantosa', label: 'LinkedIn' },
  { href: 'https://youtube.com/@samueljasonsantosa', label: 'YouTube' },
  { href: 'https://instagram.com/sammy_jason', label: 'Instagram' },
  { href: 'https://threads.net/@sammy_jason', label: 'Threads' },
  { href: 'https://tiktok.com/@samueljasons', label: 'TikTok' },
];

export const ECOSYSTEM_LINKS = [
  { href: 'https://conextlab.ai', label: 'Conextlab.ai' },
  { href: 'https://belajarai.id', label: 'BelajarAI.id' },
  { href: 'https://pekerja.ai', label: 'Pekerja.AI' },
  { href: 'https://app.conextrouter.xyz', label: 'ConextRouter' },
  { href: 'https://artifisial.com', label: 'Artifisial.com' },
  { href: 'https://n8n.io', label: 'n8n' },
];

/** Estimasi waktu baca sederhana, asumsi 200 kata per menit sesuai blog-plan 5.5. */
export function readingTime(text: string): number {
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}

const MONTHS_ID = [
  'Januari',
  'Februari',
  'Maret',
  'April',
  'Mei',
  'Juni',
  'Juli',
  'Agustus',
  'September',
  'Oktober',
  'November',
  'Desember',
];

/** Format tanggal gaya PRD: DD MMMM YYYY dalam Bahasa Indonesia. */
export function formatDateID(date: Date): string {
  return `${date.getDate()} ${MONTHS_ID[date.getMonth()]} ${date.getFullYear()}`;
}

/** Slug kategori -> label tampilan. */
export function categoryLabel(slug: string): string {
  return CATEGORIES[slug]?.label ?? slug;
}