# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class TransaksiXlsx(ReportXlsx):
    """Laporan transaksi ATK dalam format Excel (.xlsx)."""

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Transaksi')

        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Nama', bold)
        sheet.write(0, 1, 'Departemen', bold)
        sheet.write(0, 2, 'Tanggal', bold)
        sheet.write(0, 3, 'Total Harga', bold)

        row = 1
        for transaksi in lines:
            sheet.write(row, 0, transaksi.name or '')
            sheet.write(row, 1, transaksi.department_id.name or '')
            sheet.write(row, 2, transaksi.tanggal_pemesanan or '')
            sheet.write(row, 3, transaksi.total_harga or 0.0)
            row += 1

        sheet.set_column('A:A', 30)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 18)


TransaksiXlsx(
    'report.pemesanan_atk.transaksi_report_xlsx',
    'pemesanan_atk.transaksi_barang',
)