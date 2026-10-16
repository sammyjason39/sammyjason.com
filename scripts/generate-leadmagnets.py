#!/usr/bin/env python3
"""Generate the real lead-magnet PDFs for sammyjason.com.

Replaces the earlier 5-line placeholder PDFs (882 bytes) with usable, printable
one-topic worksheets. Deterministic output: same input -> same PDF bytes.

Assets:
- public/assets/downloads/ai-adoption-system-canvas.pdf   (keyword: SISTEM)
- public/assets/downloads/ai-agent-production-checklist.pdf (keyword: AGENT)
- public/assets/downloads/hermes-operator-checklist.pdf   (keyword: HERMES)

Run: python3 scripts/generate-leadmagnets.py

Requires reportlab: pip install reportlab
(Dev-only tool. The PDFs are committed, so the site build never needs reportlab.)
"""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "assets", "downloads")
os.makedirs(OUT, exist_ok=True)

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
BLUE = colors.HexColor("#1652F0")
INK = colors.HexColor("#0A0A0A")
MUTED = colors.HexColor("#555555")
LINE = colors.HexColor("#C9C9C4")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontName=FONT_B, fontSize=20, leading=24,
                    textColor=INK, alignment=TA_LEFT, spaceAfter=2)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontName=FONT, fontSize=10, leading=14,
                     textColor=MUTED, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=ss["Normal"], fontName=FONT_B, fontSize=12.5, leading=16,
                    textColor=BLUE, spaceBefore=12, spaceAfter=5)
BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontName=FONT, fontSize=9.5, leading=13.5,
                      textColor=INK, spaceAfter=5)
SMALL = ParagraphStyle("SMALL", parent=ss["Normal"], fontName=FONT, fontSize=8, leading=11,
                       textColor=MUTED)
CELL = ParagraphStyle("CELL", parent=ss["Normal"], fontName=FONT, fontSize=8.5, leading=11.5,
                      textColor=INK)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName=FONT_B)


def footer(canvas, doc, owner_line):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 15 * mm, A4[0] - 18 * mm, 15 * mm)
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 11 * mm, owner_line)
    canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, "Halaman %d" % doc.page)
    canvas.restoreState()


def build(path, title, subtitle, blocks, owner_line):
    doc = BaseDocTemplate(path, pagesize=A4, title=title, author="Samuel Jason",
                          subject=subtitle, creator="sammyjason.com")
    frame = Frame(18 * mm, 18 * mm, A4[0] - 36 * mm, A4[1] - 40 * mm, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=lambda c, d: footer(c, d, owner_line))])
    flow = [Paragraph(title, H1), Paragraph(subtitle, SUB)]
    for kind, payload in blocks:
        if kind == "h2":
            flow.append(Paragraph(payload, H2))
        elif kind == "p":
            flow.append(Paragraph(payload, BODY))
        elif kind == "small":
            flow.append(Paragraph(payload, SMALL))
        elif kind == "gap":
            flow.append(Spacer(1, payload))
        elif kind == "table":
            head, rows, widths = payload
            data = [[Paragraph(c, CELLB) for c in head]]
            for r in rows:
                data.append([Paragraph(c, CELL) for c in r])
            t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ECEAE6")),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                ("LINEAFTER", (0, 0), (-2, -1), 0.4, LINE),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]))
            flow.append(t)
    doc.build(flow)
    print("%-58s %6d bytes" % (os.path.relpath(path, ROOT), os.path.getsize(path)))


# ---------------------------------------------------------------- canvas (SISTEM)
build(
    os.path.join(OUT, "ai-adoption-system-canvas.pdf"),
    "AI Adoption System Canvas",
    "Lembar kerja untuk memilih satu proses yang layak dibantu AI sebelum membeli tool apa pun. "
    "Isi satu canvas untuk satu proses. Jangan dua.",
    [
        ("h2", "Cara pakai"),
        ("p", "Pilih satu proses yang paling banyak membuang waktu atau paling sering bocor "
              "informasi. Isi kolom kanan sejujur mungkin. Kalau ada kolom yang belum bisa "
              "dijawab, itu justru temuan: prosesnya belum siap dibantu AI."),
        ("table", (
            ["Bagian", "Isi", "Pertanyaan pemandu"],
            [
                ["1. Proses", "", "Nama proses dan seberapa sering terjadi (per hari / per minggu)."],
                ["2. Pain", "", "Waktu terbuang, error, atau informasi hilang. Ukur kasar saja."],
                ["3. Data", "", "Sumber data, siapa pemiliknya, mana yang sensitif."],
                ["4. Owner", "", "Siapa pemilik proses. Siapa yang mereview output AI."],
                ["5. Level", "", "Pilih satu: copilot, automation, atau agent. Jangan tiga."],
                ["6. Batas", "", "Apa yang boleh diakses AI. Apa yang dilarang."],
                ["7. Approval", "", "Keputusan mana yang wajib lewat manusia."],
                ["8. KPI", "", "Maksimal dua ukuran. Tentukan baseline sebelum mulai."],
                ["9. Fallback", "", "Kalau AI salah atau belum siap, siapa yang ambil alih."],
                ["10. Review", "", "Kapan dievaluasi dan siapa yang memutuskan lanjut atau stop."],
            ],
            [26, 52, 96],
        )),
        ("h2", "Skor kelayakan pilot (1 rendah sampai 5 tinggi)"),
        ("table", (
            ["Pertanyaan", "1", "2", "3", "4", "5"],
            [
                ["Seberapa sering pekerjaan ini terjadi?", "", "", "", "", ""],
                ["Seberapa besar pain atau waktu yang habis?", "", "", "", "", ""],
                ["Seberapa siap data dan SOP-nya?", "", "", "", "", ""],
                ["Seberapa mudah hasilnya diukur?", "", "", "", "", ""],
                ["Seberapa rendah risiko kalau pilot gagal?", "", "", "", "", ""],
            ],
            [110, 12, 12, 12, 12, 12],
        )),
        ("small", "Pilih use case dengan frekuensi tinggi, pain nyata, SOP stabil, hasil "
                  "terukur, dan risiko terkendali. Itu biasanya bukan use case paling keren."),
        ("h2", "Roadmap 90 hari"),
        ("table", (
            ["Fase", "Fokus", "Selesai kalau"],
            [
                ["Hari 1 sampai 30",
                 "Audit 3 sampai 5 proses. Tetapkan aturan data dan approval. Latih satu cohort kecil berdasarkan peran. Pilih 1 sampai 2 pilot.",
                 "Ada baseline dan KPI tertulis sebelum pilot jalan."],
                ["Hari 31 sampai 60",
                 "Jalankan pilot di workflow nyata. Catat kegagalan, override manusia, dan rework.",
                 "Ada keputusan eksplisit: lanjut, perbaiki, hentikan, atau ganti pendekatan."],
                ["Hari 61 sampai 90",
                 "Integrasikan yang terbukti. Tetapkan process owner, training, review cadence, monitoring.",
                 "Sistemnya yang di-scale, bukan cuma tool-nya."],
            ],
            [26, 88, 60],
        )),
        ("h2", "Contoh terisi: follow-up lead masuk"),
        ("table", (
            ["Bagian", "Isi contoh"],
            [
                ["Proses", "Lead dari form website dan DM dihubungi pertama kali. Sekitar 40 per minggu."],
                ["Pain", "Rata-rata 9 jam sampai kontak pertama. Sebagian lead tidak pernah dihubungi."],
                ["Data", "Form website, WhatsApp Business, spreadsheet sales. Nomor telepon sensitif."],
                ["Owner", "Sales lead sebagai pemilik proses. Sales ops mereview output klasifikasi."],
                ["Level", "Copilot. Bukan agent, karena balasan ke calon customer masih manual."],
                ["Batas", "AI boleh merangkum dan mengklasifikasi. AI tidak boleh menghubungi customer langsung."],
                ["Approval", "Semua pesan keluar wajib disetujui manusia."],
                ["KPI", "Waktu kontak pertama, dan persentase lead yang dihubungi dalam 1 jam kerja."],
                ["Fallback", "Kalau klasifikasi ragu, masuk antrean manual tanpa label."],
                ["Review", "Evaluasi mingguan oleh sales lead. Keputusan lanjut di pekan keempat."],
            ],
            [26, 148],
        )),
        ("h2", "Yang tidak boleh dilakukan"),
        ("p", "Jangan mulai dari daftar tools. Jangan beli lisensi massal tanpa aturan main. "
              "Jangan beri AI akses ke data pelanggan tanpa batas yang tertulis. Jangan ukur "
              "keberhasilan dari jumlah percobaan prompt."),
    ],
    "AI Adoption System Canvas - Samuel Jason - sammyjason.com - diperbarui 16 Oktober 2026",
)

# ------------------------------------------------------- agent checklist (AGENT)
build(
    os.path.join(OUT, "ai-agent-production-checklist.pdf"),
    "AI Agent Production Readiness Checklist",
    "Daftar periksa sebelum sebuah AI agent diberi akses ke sistem atau pelanggan nyata. "
    "Kalau ada satu bagian belum tercentang, agent-nya belum layak produksi.",
    [
        ("h2", "1. Lima syarat dasar"),
        ("table", (
            ["Syarat", "Terpenuhi kalau", "Siap?"],
            [
                ["Job jelas", "Agent punya satu pekerjaan yang bisa ditulis dalam satu kalimat dan punya ukuran hasil.", ""],
                ["Data jelas", "Sumber data tertulis, ada pemilik, dan ada aturan mana yang tidak boleh masuk.", ""],
                ["Batas akses", "Daftar tool yang boleh dipakai tertulis eksplisit. Sisanya ditolak, bukan diabaikan.", ""],
                ["Approval manusia", "Ada titik keputusan yang wajib lewat manusia sebelum efek permanen.", ""],
                ["Monitoring", "Ada log, trace, dan cara tahu ketika agent gagal atau looping.", ""],
            ],
            [30, 128, 16],
        )),
        ("h2", "2. Kontrak tool"),
        ("table", (
            ["Area", "Yang harus ada", "Siap?"],
            [
                ["Skema", "Setiap tool punya skema input yang tervalidasi. Tidak ada argumen bebas.", ""],
                ["Izin", "Tool dibatasi ke pemanggil yang berhak. Tidak ada akses global demi kenyamanan.", ""],
                ["Efek samping", "Operasi yang mengubah data dipisah dari yang hanya membaca.", ""],
                ["Idempotensi", "Pemanggilan ulang dengan argumen sama tidak menggandakan efek.", ""],
            ],
            [30, 128, 16],
        )),
        ("h2", "3. Kendali biaya dan kegagalan"),
        ("table", (
            ["Kendali", "Nilai yang harus ditetapkan lebih dulu", "Nilai"],
            [
                ["Batas langkah", "Jumlah maksimum langkah atau pemanggilan tool per tugas.", ""],
                ["Batas biaya", "Plafon token atau rupiah per tugas dan per hari.", ""],
                ["Circuit breaker", "Berapa kegagalan beruntun sebelum agent dihentikan.", ""],
                ["Timeout", "Batas waktu per langkah dan per tugas.", ""],
                ["Retry", "Berapa kali dicoba ulang, dan syarat apa yang membuatnya berhenti.", ""],
            ],
            [30, 128, 16],
        )),
        ("h2", "4. Observability"),
        ("table", (
            ["Pertanyaan", "Ya", "Tidak"],
            [
                ["Bisa merekonstruksi satu tugas lengkap dari log?", "", ""],
                ["Bisa melihat biaya per tugas, bukan hanya total bulanan?", "", ""],
                ["Bisa melihat di langkah mana tugas gagal?", "", ""],
                ["Ada peringatan otomatis ketika agent gagal berulang?", "", ""],
                ["Tersimpan alasan ketika manusia meng-override hasil agent?", "", ""],
            ],
            [120, 20, 22],
        )),
        ("h2", "5. Guardrail perilaku"),
        ("p", "Tulis batas yang eksplisit: apa yang agent dilarang lakukan meskipun diminta, "
              "data apa yang tidak boleh dikirim ke model publik, dan kapan agent wajib berhenti "
              "dan bertanya. Batas yang hanya ada di prompt bukan batas. Batas yang benar "
              "ditegakkan di kode."),
        ("h2", "6. Gerbang rilis"),
        ("table", (
            ["Gerbang", "Bukti yang dikumpulkan", "Lulus?"],
            [
                ["Uji di lingkungan terbatas", "Hasil uji dengan input acak, bukan hanya contoh rapi.", ""],
                ["Uji override manusia", "Bukti bahwa manusia bisa menghentikan agent kapan saja.", ""],
                ["Uji fallback", "Bukti bahwa kegagalan model berakhir di jalur deterministik.", ""],
                ["Rencana rilis", "Ada pemilik, jadwal evaluasi, dan kriteria rollback.", ""],
            ],
            [40, 118, 16],
        )),
        ("h2", "Catatan operator"),
        ("p", "Agent produksi itu kira-kira sepuluh persen model dan sembilan puluh persen "
              "pagar pengaman. Kalau demo-nya bagus tapi checklist ini belum penuh, yang kamu "
              "punya bukan agent. Yang kamu punya chatbot mahal dengan akses berlebih."),
    ],
    "AI Agent Production Readiness Checklist - Samuel Jason - sammyjason.com - diperbarui 16 Oktober 2026",
)

# ------------------------------------------------------ hermes operator (HERMES)
build(
    os.path.join(OUT, "hermes-operator-checklist.pdf"),
    "VPS Setup Checklist dan Template Konfigurasi Aman",
    "Urutan kerja untuk menjalankan model open-weight di VPS sendiri tanpa server tumbang "
    "dan tanpa port terbuka ke internet.",
    [
        ("h2", "1. Sebelum menyentuh instalasi"),
        ("table", (
            ["Periksa", "Target", "Siap?"],
            [
                ["Spesifikasi", "Catat RAM, vCPU, disk, dan apakah ada GPU. Tentukan batas model.", ""],
                ["Akses", "Ada akses SSH dengan kunci, bukan kata sandi.", ""],
                ["Pulih", "Ada cara membangun ulang server ini dari nol tanpa panik.", ""],
                ["Anggaran", "Ada batas biaya bulanan yang ditulis, bukan diperkirakan sambil jalan.", ""],
            ],
            [30, 128, 16],
        )),
        ("h2", "2. Urutan instalasi"),
        ("table", (
            ["Langkah", "Yang dilakukan", "Selesai kalau"],
            [
                ["1", "Perbarui paket sistem dan buat pengguna non-root untuk menjalankan aplikasi.", "Aplikasi tidak jalan sebagai root."],
                ["2", "Pasang runtime dan dependensi dengan versi yang dipin.", "Versi tercatat, bukan versi terbaru apa saja."],
                ["3", "Unduh bobot model dan simpan di direktori data terpisah.", "Bobot tidak bercampur dengan kode."],
                ["4", "Letakkan konfigurasi di berkas environment, bukan di argumen perintah.", "Tidak ada rahasia yang menempel di riwayat perintah."],
                ["5", "Batasi sumber daya: memori, CPU, dan proses bersamaan.", "Ada plafon yang tertulis dan diuji."],
                ["6", "Jalankan sebagai layanan dengan restart otomatis.", "Layanan hidup lagi setelah reboot."],
                ["7", "Letakkan reverse proxy di depan layanan.", "Port aplikasi hanya menerima dari localhost."],
                ["8", "Pasang sertifikat TLS dan paksa HTTPS.", "HTTP biasa dialihkan, bukan melayani."],
                ["9", "Verifikasi dari luar.", "Endpoint menjawab sehat, port internal tertutup."],
            ],
            [16, 88, 70],
        )),
        ("h2", "3. Konfigurasi yang paling sering salah"),
        ("table", (
            ["Kesalahan", "Akibatnya", "Perbaikannya"],
            [
                ["Binding ke 0.0.0.0 hanya demi mudah dites", "Layanan terbuka ke internet", "Binding ke 127.0.0.1, akses lewat proxy"],
                ["Menempelkan kunci API di baris perintah", "Rahasia masuk riwayat shell dan log", "Pakai berkas environment dengan izin terbatas"],
                ["Tanpa batas memori", "Server tumbang saat beban naik", "Pasang plafon memori dan uji sampai batasnya"],
                ["Tanpa batas konkurensi", "Antrean menumpuk, waktu jawab ambruk", "Batasi permintaan bersamaan"],
                ["Log tanpa rotasi", "Disk penuh dalam hitungan pekan", "Aktifkan rotasi dan batas ukuran log"],
            ],
            [52, 50, 72],
        )),
        ("h2", "4. Verifikasi setelah naik"),
        ("table", (
            ["Uji", "Cara", "Hasil yang diharapkan"],
            [
                ["Kesehatan layanan", "Panggil endpoint sehat dari server itu sendiri.", "Jawaban sehat dan cepat."],
                ["Isolasi port", "Coba akses port aplikasi dari mesin lain.", "Koneksi ditolak."],
                ["Paksa HTTPS", "Akses lewat HTTP biasa.", "Dialihkan ke HTTPS."],
                ["Pulih setelah reboot", "Reboot lalu tunggu beberapa menit.", "Layanan hidup tanpa campur tangan."],
                ["Beban wajar", "Kirim beberapa permintaan berurutan.", "Waktu jawab stabil, tidak ada proses yang dimatikan sistem."],
            ],
            [36, 78, 60],
        )),
        ("h2", "5. Sebelum dipakai kerja nyata"),
        ("p", "Tentukan siapa yang boleh memakainya, data apa yang boleh masuk, dan bagaimana "
              "log ditinjau. Server yang rapi tapi tanpa aturan data hanya memindahkan masalah "
              "ke tempat yang lebih sulit dilihat."),
        ("small", "Catatan: jalankan satu perubahan pada satu waktu, lalu verifikasi. "
                  "Perubahan bertumpuk membuat penyebab kegagalan tidak bisa dilacak."),
    ],
    "VPS Setup Checklist dan Template Konfigurasi Aman - Samuel Jason - sammyjason.com - diperbarui 16 Oktober 2026",
)
