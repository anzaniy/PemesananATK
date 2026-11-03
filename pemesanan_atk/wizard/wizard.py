# -*- coding: utf-8 -*-

import base64
from StringIO import StringIO

import xlsxwriter
from odoo import models, fields, api


class WizardRekapanLaporan(models.TransientModel):
    _name = 'pemesanan_atk.wizard_rekapan_laporan'
    _description = 'Rekap Laporan Pemesanan ATK'

    name = fields.Char("Nama File")
    file = fields.Binary("File", readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('rfa', 'Diajukan'),
        ('approved', 'Disetujui'),
        ('reject', 'Ditolak'),
    ], string="Status", required=True)
    start_date = fields.Date(string="Dari Tanggal", required=True)
    end_date = fields.Date(string="Sampai Tanggal", required=True)

    @api.multi
    def _add_workbook_format(self, workbook):
        wbf = {}
        wbf['company'] = workbook.add_format({
            'bold': 1, 'align': 'left', 'font_color': '#000000',
            'num_format': 'dd-mm-yyyy'})
        wbf['company'].set_font_size(12)

        wbf['header'] = workbook.add_format({
            'bg_color': '#FFFF00', 'bold': 1, 'align': 'center',
            'font_color': '#000000'})
        wbf['header'].set_top(2)
        wbf['header'].set_bottom()
        wbf['header'].set_left()
        wbf['header'].set_right()
        wbf['header'].set_font_size(11)
        wbf['header'].set_align('vcenter')

        wbf['header_left'] = workbook.add_format({
            'bg_color': '#FFFF00', 'bold': 1, 'align': 'center',
            'font_color': '#000000'})
        wbf['header_left'].set_top(2)
        wbf['header_left'].set_bottom()
        wbf['header_left'].set_left(2)
        wbf['header_left'].set_right()
        wbf['header_left'].set_font_size(11)
        wbf['header_left'].set_align('vcenter')

        wbf['header_right'] = workbook.add_format({
            'bg_color': '#FFFF00', 'bold': 1, 'align': 'center',
            'font_color': '#000000'})
        wbf['header_right'].set_top(2)
        wbf['header_right'].set_bottom()
        wbf['header_right'].set_left()
        wbf['header_right'].set_right(2)
        wbf['header_right'].set_font_size(11)
        wbf['header_right'].set_align('vcenter')

        wbf['content'] = workbook.add_format({'align': 'left', 'font_color': '#000000'})
        wbf['content'].set_left()
        wbf['content'].set_right()
        wbf['content'].set_top()
        wbf['content'].set_bottom()
        wbf['content'].set_font_size(10)

        wbf['content_left'] = workbook.add_format({'align': 'center', 'font_color': '#000000'})
        wbf['content_left'].set_left(2)
        wbf['content_left'].set_right()
        wbf['content_left'].set_top()
        wbf['content_left'].set_bottom()
        wbf['content_left'].set_font_size(10)

        wbf['content_right'] = workbook.add_format({'align': 'center', 'font_color': '#000000'})
        wbf['content_right'].set_left()
        wbf['content_right'].set_right(2)
        wbf['content_right'].set_top()
        wbf['content_right'].set_bottom()
        wbf['content_right'].set_font_size(10)

        wbf['content_center_bg_bottom'] = workbook.add_format({
            'bg_color': '#85C1E9', 'align': 'center', 'font_color': '#000000'})
        wbf['content_center_bg_bottom'].set_left()
        wbf['content_center_bg_bottom'].set_right()
        wbf['content_center_bg_bottom'].set_top()
        wbf['content_center_bg_bottom'].set_bottom(2)
        wbf['content_center_bg_bottom'].set_font_size(10)
        return wbf

    @api.multi
    def cetak_rekapan(self):
        self.ensure_one()
        fp = StringIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf = self._add_workbook_format(workbook)
        worksheet = workbook.add_worksheet('Rekapan Laporan')

        worksheet.set_column('B1:B1', 4)
        worksheet.set_column('C1:C1', 20)
        worksheet.set_column('D1:D1', 20)
        worksheet.set_column('E1:E1', 20)
        worksheet.set_column('F1:F1', 20)

        self.env.cr.execute("""
            SELECT b.name, b.harga_barang, SUM(l.jumlah), SUM(l.total_harga)
              FROM pemesanan_atk_transaksi_line l
              JOIN pemesanan_atk_barang_atk b ON b.id = l.barang_id
              JOIN pemesanan_atk_transaksi_barang t ON t.id = l.transaksi_id
             WHERE t.state = %s
               AND t.tanggal_pemesanan BETWEEN %s AND %s
             GROUP BY b.name, b.harga_barang
             ORDER BY b.name
        """, (self.state, self.start_date, self.end_date))
        ress = self.env.cr.fetchall()

        worksheet.merge_range('B1:F1', 'Rekapitulasi Pemesanan ATK', wbf['company'])
        worksheet.merge_range('B2:F2', 'Tanggal : %s s/d %s' % (
            self.start_date, self.end_date), wbf['company'])
        worksheet.merge_range('B3:F3', 'Status : %s' % self.state, wbf['company'])

        row = 3
        worksheet.write('B%s' % (row + 1), 'No', wbf['header_left'])
        worksheet.write('C%s' % (row + 1), 'Nama Barang', wbf['header'])
        worksheet.write('D%s' % (row + 1), 'Harga Satuan', wbf['header'])
        worksheet.write('E%s' % (row + 1), 'Jumlah', wbf['header'])
        worksheet.write('F%s' % (row + 1), 'Harga Total', wbf['header_right'])
        row += 2

        if not ress:
            worksheet.merge_range('B%s:F%s' % (row, row), 'Data tidak ada!', wbf['content'])
        no = 1
        for res in ress:
            worksheet.write('B%s' % row, no, wbf['content_left'])
            worksheet.write('C%s' % row, res[0], wbf['content'])
            worksheet.write('D%s' % row, res[1], wbf['content'])
            worksheet.write('E%s' % row, res[2], wbf['content'])
            worksheet.write('F%s' % row, res[3], wbf['content_right'])
            row += 1
            no += 1

        worksheet.merge_range('B%s:E%s' % (row, row), 'Total',
                              wbf['content_center_bg_bottom'])
        worksheet.write('F%s' % row, '=SUM(F5:F%s)' % (row - 1),
                        wbf['content_center_bg_bottom'])
        workbook.close()

        self.write({
            'file': base64.encodestring(fp.getvalue()),
            'name': 'Rekapan Laporan.xlsx',
        })
        fp.close()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/pemesanan_atk.wizard_rekapan_laporan/%s/file/%s?download=true'
                   % (self.id, self.name),
            'name': 'Rekapan Laporan',
        }