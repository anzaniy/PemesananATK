# Pemesanan ATK — Odoo 10

Modul Odoo 10 untuk pengajuan alat tulis kantor (ATK): master barang dan
departemen, transaksi dengan alur persetujuan, validasi stok, serta laporan PDF
dan Excel.

```
Draft  ->  Diajukan (RFA)  ->  Disetujui
                          \->  Ditolak
```

Dibuat sebagai proyek individu, bukan bagian dari modul perusahaan mana pun.

## Isi repo

| Path | Keterangan |
|---|---|
| `pemesanan_atk/` | Modul Odoo (folder ini yang dipasang ke addons) |
| `pemesanan_atk/README.md` | Dokumentasi modul: fitur, instalasi, penggunaan |
| `pemesanan_atk/LICENSE` | LGPL-3 |

## Instalasi singkat

Prasyarat: Odoo 10 dan modul [OCA `report_xlsx`](https://github.com/OCA/reporting-engine)
versi 10.0.

```bash
git clone https://github.com/anzaniy/PemesananATK.git
# salin folder pemesanan_atk ke direktori addons, lalu:
odoo-bin -c odoo.conf -d nama_database -i pemesanan_atk --stop-after-init
```

Setelah terpasang, berikan grup **Pemesanan ATK / Manager** kepada user yang
akan menyetujui pengajuan (Settings > Users).

## Fitur

- Master barang (nama, stok, harga, aktif/nonaktif) dan master departemen
- Transaksi header + rincian barang, total dihitung otomatis
- Alur status Draft / Diajukan / Disetujui / Ditolak dengan tombol per grup
- Validasi jumlah terhadap stok
- Grup User dan Manager, record rule per pemilik data
- Laporan PDF (QWeb), laporan Excel per transaksi, dan rekap Excel per status
  dengan rentang tanggal

Rincian lengkap ada di [`pemesanan_atk/README.md`](pemesanan_atk/README.md).

## Lisensi

LGPL-3 — lihat [`pemesanan_atk/LICENSE`](pemesanan_atk/LICENSE).
