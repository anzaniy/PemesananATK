# Pemesanan ATK

An Odoo 10 module for office stationery (ATK) requests: item and department
masters, a transaction approval workflow, stock validation, and PDF/Excel
reports.

## Background

Many teams still request stationery over chat or spreadsheets, so stock is not
controlled and there is no record of who approved what. This module makes the
flow explicit:

```
Draft  ->  Submitted (RFA)  ->  Approved
                            \->  Rejected
```

- A **User** creates requests and only sees their own.
- A **Manager ATK** maintains the item and department masters and approves or
  rejects requests.
- A requested quantity may not exceed the recorded stock.

## Features

| Feature | Description |
|---|---|
| Item master | Name, stock, price, active flag |
| Department master | List of requesting departments |
| Transaction | Header + item lines, total computed automatically |
| Status flow | Draft, Submitted, Approved, Rejected |
| Stock validation | Quantity re-validated when the item changes |
| Access rights | User and Manager groups, record rules per data owner |
| PDF report | QWeb, per transaction |
| Excel report | `.xlsx` per transaction (via `report_xlsx`) |
| Excel recap | Recap per status and date range |

## Installation

Requirements: Odoo 10 and the
[OCA `report_xlsx`](https://github.com/OCA/reporting-engine) module, version 10.0.

1. Copy the `pemesanan_atk` folder into your Odoo addons directory.
2. Add that directory to `addons_path` in `odoo.conf`.
3. Restart the Odoo service.
4. Open **Apps**, click **Update Apps List**, then install **Pemesanan ATK**.

Via CLI:

```bash
odoo-bin -c odoo.conf -d your_database -i pemesanan_atk --stop-after-init
```

On Windows the binary is `odoo-bin.exe` and its path contains spaces, so it
must be fully quoted:

```powershell
& "C:\Program Files (x86)\Odoo 10.0\server\odoo-bin.exe" `
  -c "C:\Program Files (x86)\Odoo 10.0\server\odoo.conf" `
  -d your_database --xmlrpc-port=8071 -i pemesanan_atk --stop-after-init
```

- Use `-u` instead of `-i` when the module is already installed and you only
  want to update it.
- `--xmlrpc-port` is needed when another Odoo service is already using 8069.
- A freshly installed database contains no data (no items or departments), so
  fill in **Master > Barang ATK** (items) and **Master > Departemen**
  (departments) first.

After installation, assign the **Pemesanan ATK / Manager** group to the user
who will approve requests (Settings > Users).

## Usage

1. **Master > Barang ATK** — enter items, stock, and prices.
2. **Master > Departemen** — enter the department list.
3. **Transaksi > Form Transaksi** — create a request, add item lines, then
   click **Ajukan** (Submit).
4. **Setujui / Tolak** (Approve / Reject) — only visible to Manager ATK.
5. **Cetak PDF / Cetak Excel** — per-transaction reports.
6. **Laporan > Rekap Laporan** — pick a status and date range, then click
   **Buat Rekap** (Generate Recap).

## Structure

```
pemesanan_atk/
├── models/
│   ├── department.py        # pemesanan_atk.department
│   ├── transaksi.py         # transaction, item, lines
│   └── cetak_laporan.py     # Excel report (report_xlsx)
├── wizard/
│   └── wizard.py            # recap by status + date range
├── views/                   # menus, departments, items, transactions
├── security/                # groups, model access, record rules
├── report/                  # QWeb PDF + report definitions
└── static/description/      # module icon
```

## License

LGPL-3. See [LICENSE](LICENSE).