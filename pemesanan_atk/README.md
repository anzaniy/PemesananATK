# Pemesanan ATK

Modul Odoo 10 untuk pengajuan alat tulis kantor (ATK): master barang dan
departemen, transaksi dengan alur persetujuan, validasi stok, dan laporan
PDF/Excel.

## Latar belakang

Banyak tim masih mengajukan ATK lewat chat atau spreadsheet, sehingga stok tidak
terkontrol dan tidak ada jejak siapa yang menyetujui apa. Modul ini membuat
alurnya eksplisit:

```
Draft  ->  Diajukan (RFA)  ->  Disetujui
                          \->  Ditolak
```

- **User** membuat pengajuan dan hanya melihat pengajuannya sendiri.
- **Manager ATK** mengelola master barang/departemen dan menyetujui atau
  menolak pengajuan.
- Jumlah yang diminta tidak boleh melebihi stok yang tercatat.

## Fitur

| Fitur | Keterangan |
|---|---|
| Master barang | Nama, stok, harga, aktif/nonaktif |
| Master departemen | Daftar departemen pemesan |
| Transaksi | Header + rincian barang, total dihitung otomatis |
| Alur status | Draft, Diajukan, Disetujui, Ditolak |
| Validasi stok | Jumlah divalidasi ulang saat barang diganti |
| Hak akses | Grup User dan Manager, record rule per pemilik data |
| Laporan PDF | QWeb, per transaksi |
| Laporan Excel | `.xlsx` per transaksi (via `report_xlsx`) |
| Rekap Excel | Rekap per status dan rentang tanggal |

## Instalasi

Prasyarat: Odoo 10 dan modul [OCA `report_xlsx`](https://github.com/OCA/reporting-engine)
versi 10.0.

1. Salin folder `pemesanan_atk` ke direktori addons Odoo.
2. Tambahkan direktori tersebut ke `addons_path` di `odoo.conf`.
3. Restart service Odoo.
4. Buka **Apps**, klik **Update Apps List**, lalu install **Pemesanan ATK**.

Via CLI:

```bash
odoo-bin -c odoo.conf -d nama_database -i pemesanan_atk --stop-after-init
```

Di Windows nama binary-nya `odoo-bin.exe` dan path-nya mengandung spasi, jadi
perlu dikutip penuh:

```powershell
& "C:\Program Files (x86)\Odoo 10.0\server\odoo-bin.exe" `
  -c "C:\Program Files (x86)\Odoo 10.0\server\odoo.conf" `
  -d nama_database --xmlrpc-port=8071 -i pemesanan_atk --stop-after-init
```

- Ganti `-i` menjadi `-u` kalau modul sudah terpasang dan hanya ingin
  memperbarui.
- `--xmlrpc-port` perlu ditambah kalau service Odoo lain sedang memakai 8069.
- Database baru hasil instal berisi data kosong (belum ada barang/departemen),
  jadi isi dulu **Master > Barang ATK** dan **Master > Departemen**.

Setelah terpasang, berikan grup **Pemesanan ATK / Manager** kepada user yang
akan menyetujui pengajuan (Settings > Users).

## Penggunaan

1. **Master > Barang ATK** — isi barang, stok, dan harga.
2. **Master > Departemen** — isi daftar departemen.
3. **Transaksi > Form Transaksi** — buat pengajuan, tambahkan rincian barang,
   lalu klik **Ajukan**.
4. **Setujui / Tolak** — hanya muncul untuk Manager ATK.
5. **Cetak PDF / Cetak Excel** — laporan per transaksi.
6. **Laporan > Rekap Laporan** — pilih status dan rentang tanggal, lalu
   **Buat Rekap**.

## Struktur

```
pemesanan_atk/
├── models/
│   ├── department.py        # pemesanan_atk.department
│   ├── transaksi.py         # transaksi, barang, rincian
│   └── cetak_laporan.py     # laporan Excel (report_xlsx)
├── wizard/
│   └── wizard.py            # rekap per status + rentang tanggal
├── views/                   # menu, departemen, barang, transaksi
├── security/                # grup, akses model, record rule
├── report/                  # QWeb PDF + definisi report
└── static/description/      # ikon modul
```

## Lisensi

LGPL-3. Lihat [LICENSE](LICENSE).