# Pemesanan ATK — Odoo 10

An Odoo 10 module for office stationery (ATK) requests: item and department
masters, a transaction approval workflow, stock validation, and PDF/Excel
reports.

```
Draft  ->  Submitted (RFA)  ->  Approved
                            \->  Rejected
```

Built as an individual project, not part of any company's module.

## Quick install

Requirements: Odoo 10 and the
[OCA `report_xlsx`](https://github.com/OCA/reporting-engine) module, version 10.0.

```bash
git clone https://github.com/anzaniy/PemesananATK.git
# copy the pemesanan_atk folder into your addons directory, then:
odoo-bin -c odoo.conf -d your_database -i pemesanan_atk --stop-after-init
```

After installation, assign the **Pemesanan ATK / Manager** role to the user
who will approve requests (Settings > Users).

## Features

- Item master (name, stock, price, active flag) and department master
- Transaction header + item lines, total computed automatically
- Draft / Submitted / Approved / Rejected status flow with per-group buttons
- Quantity validation against stock
- User and Manager groups, record rules per data owner
- PDF report (QWeb), Excel report per transaction, and Excel recap per status
  with a date range

Full details are in [`pemesanan_atk/README.md`](pemesanan_atk/README.md).

## License

LGPL-3 — see [`pemesanan_atk/LICENSE`](pemesanan_atk/LICENSE).