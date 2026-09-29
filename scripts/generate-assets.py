#!/usr/bin/env python3
"""Generate static image assets for sammyjason.com:
- public/og.png (1200x630) default OpenGraph card
- public/images/blog/<slug>.webp (1600x900) article hero images
Light cement-gray theme, Conextlab blue accents, no external fonts (DejaVu Sans bundled).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
os.makedirs(os.path.join(PUBLIC, 'images', 'blog'), exist_ok=True)
os.makedirs(os.path.join(PUBLIC, 'og'), exist_ok=True)

W, H = 1200, 630
HERO_W, HERO_H = 1600, 900

DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
DEJAVU_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

GREEN = (22, 82, 240)
BLUE = (30, 64, 175)
NIGHT = (245, 245, 244)
PANEL = (236, 234, 230)
INK = (10, 10, 10)
SOFT_BLUE = (110, 142, 250)
SOFT_TEXT = (30, 64, 175)


def vertical_gradient(w, h, top, bottom):
    img = Image.new('RGB', (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def diagonal_gradient(w, h, c1, c2):
    """Diagonal gradient (top-left c1 -> bottom-right c2)."""
    img = Image.new('RGB', (w, h))
    px = img.load()
    for y in range(h):
        for x in range(0, w):
            t = (x / max(1, w - 1) + y / max(1, h - 1)) / 2
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return img


def overlay_radial(img, center, radius, color, alpha_peak=70):
    """Soft radial glow overlay."""
    glow = Image.new('L', img.size, 0)
    gd = ImageDraw.Draw(glow)
    cx, cy = center
    steps = 24
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(alpha_peak * (1 - i / steps) ** 1.5)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    overlay = Image.new('RGB', img.size, color)
    img.paste(Image.composite(overlay, img, glow), (0, 0))
    return img


def draw_monogram(img, cx, cy, r, ring=True):
    d = ImageDraw.Draw(img)
    # gradient circle via mask
    size = r * 2
    grad = diagonal_gradient(size, size, (22, 82, 240), (10, 10, 10))
    mask = Image.new('L', (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, size, size], fill=255)
    img.paste(grad, (cx - r, cy - r), mask)
    if ring:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 229, 254, 110), width=6)
    f = ImageFont.truetype(DEJAVU_BOLD, int(r * 0.72))
    bbox = d.textbbox((0, 0), 'SJ', font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), 'SJ', font=f, fill=(255, 255, 255))


def footer_line(d, w, h, tagline):
    f_small = ImageFont.truetype(DEJAVU, 26)
    d.text((80, h - 90), 'samueljason  ·  sammyjason.com', font=f_small, fill=(107, 114, 128))
    d.text((80, h - 56), tagline, font=f_small, fill=SOFT_TEXT)


def make_og(title_lines, category=None, out='og.png', w=W, h=H, monogram_r=110):
    img = diagonal_gradient(w, h, NIGHT, PANEL)
    img = overlay_radial(img, (int(w * 0.88), int(h * 0.06)), int(w * 0.5), SOFT_BLUE, alpha_peak=36)
    img = overlay_radial(img, (int(w * 0.02), int(h * 1.02)), int(w * 0.42), SOFT_BLUE, alpha_peak=30)
    d = ImageDraw.Draw(img)

    # monogram avatar
    draw_monogram(img, w - 80 - monogram_r, 80 + monogram_r, monogram_r)

    # category pill
    y = 92
    if category:
        f_cat = ImageFont.truetype(DEJAVU_BOLD, 30)
        bbox = d.textbbox((0, 0), category, font=f_cat)
        tw = bbox[2] - bbox[0]
        pad_x, pad_y = 26, 14
        d.rounded_rectangle(
            [80, y, 80 + tw + pad_x * 2, y + 30 + bbox[1] + bbox[3] + pad_y * 2],
            radius=999,
            fill=(220, 229, 254, 160),
            outline=(30, 64, 175),
            width=2,
        )
        d.text((80 + pad_x, y + pad_y - bbox[1] + 4), category, font=f_cat, fill=SOFT_TEXT)
        y += 30 + bbox[1] + bbox[3] + pad_y * 2 + 36

    # title lines
    f_title = ImageFont.truetype(DEJAVU_BOLD, 64)
    line_h = 84
    for line in title_lines:
        d.text((80, y), line, font=f_title, fill=INK)
        y += line_h

    # accent bar
    d.rectangle([80, y + 18, 80 + 120, y + 24], fill=GREEN)

    footer_line(d, w, h, '"Teman kamu bertumbuh di Era AI."')
    img.save(os.path.join(PUBLIC, out), 'PNG', optimize=True)
    print(f'wrote public/{out} ({w}x{h})')


def make_hero(slug, title_lines, category, out):
    w, h = HERO_W, HERO_H
    img = diagonal_gradient(w, h, NIGHT, PANEL)
    img = overlay_radial(img, (int(w * 0.85), int(h * 0.1)), int(w * 0.45), SOFT_BLUE, alpha_peak=34)
    img = overlay_radial(img, (int(w * 0.05), int(h * 0.95)), int(w * 0.4), SOFT_BLUE, alpha_peak=28)
    d = ImageDraw.Draw(img)

    draw_monogram(img, w - 70 - 130, 70 + 130, 130)

    f_cat = ImageFont.truetype(DEJAVU_BOLD, 34)
    d.text((90, 110), category.upper(), font=f_cat, fill=SOFT_TEXT)

    y = 190
    f_title = ImageFont.truetype(DEJAVU_BOLD, 78)
    line_h = 102
    for line in title_lines:
        d.text((90, y), line, font=f_title, fill=INK)
        y += line_h

    d.rectangle([90, y + 24, 90 + 150, y + 32], fill=GREEN)

    f_small = ImageFont.truetype(DEJAVU, 30)
    d.text((90, h - 110), 'samueljason  ·  sammyjason.com/blog', font=f_small, fill=(107, 114, 128))

    path = os.path.join(PUBLIC, 'images', 'blog', out)
    img.save(path, 'WEBP', quality=82, method=6)
    print(f'wrote public/images/blog/{out} ({w}x{h})')


if __name__ == '__main__':
    make_og(
        ['Catatan Lapangan', '& Rekayasa AI'],
        category=None,
        out='og.png',
    )
    # OG card 1200x630 per artikel (PRD 5.2: og:image statis 1200x630)
    make_og(
        ['Setup Hermes Free,', 'But Do It Like an Operator'],
        category='Build Logs',
        out='og/setup-hermes-free-operator.png',
        monogram_r=92,
    )
    make_og(
        ['Adaptasi AI Mulai', 'dari Alur Kerja,', 'Bukan Beli Tools'],
        category='Framework 4M',
        out='og/perusahaan-mulai-adaptasi-ai-alur-kerja.png',
        monogram_r=92,
    )
    make_og(
        ['Anatomi AI Agent', 'di Lingkungan Produksi'],
        category='Catatan CTO',
        out='og/anatomi-ai-agent-produksi-conextlab.png',
        monogram_r=92,
    )
    make_hero(
        'setup-hermes-free-operator',
        ['Setup Hermes Free,', 'But Do It Like', 'an Operator'],
        'Build Logs',
        'setup-hermes-free-operator.webp',
    )
    make_hero(
        'perusahaan-mulai-adaptasi-ai-alur-kerja',
        ['Adaptasi AI Mulai', 'dari Alur Kerja,', 'Bukan Beli Tools'],
        'Framework 4M',
        'perusahaan-mulai-adaptasi-ai-alur-kerja.webp',
    )
    make_hero(
        'anatomi-ai-agent-produksi-conextlab',
        ['Anatomi AI Agent', 'di Lingkungan', 'Produksi'],
        'Catatan CTO',
        'anatomi-ai-agent-produksi-conextlab.webp',
    )
    print('done')