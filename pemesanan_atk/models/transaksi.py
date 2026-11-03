# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError


class Transaksi(models.Model):
    _name = 'pemesanan_atk.transaksi_barang'
    _description = 'Transaksi Pemesanan ATK'
    _order = 'tanggal_pemesanan desc, id desc'

    name = fields.Char(string='No. Dokumen', required=True)
    department_id = fields.Many2one('pemesanan_atk.department', string='Departemen')
    transaksi_line_ids = fields.One2many(
        'pemesanan_atk.transaksi_line', 'transaksi_id', string='Rincian Barang')
    total_harga = fields.Float(string='Total Harga', compute='_compute_total_harga')
    tanggal_pemesanan = fields.Date(
        string='Tanggal Pemesanan', required=True, default=fields.Date.context_today)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('rfa', 'Diajukan'),
        ('approved', 'Disetujui'),
        ('reject', 'Ditolak'),
    ], string='Status', readonly=True, copy=False, default='draft')

    @api.multi
    def write(self, vals):
        target = vals.get('state')
        if target:
            for transaksi in self:
                if transaksi.state == target:
                    continue
                if transaksi.state == 'draft' and target == 'rfa':
                    continue
                if transaksi.state == 'rfa' and target in ('approved', 'reject'):
                    if not self.env.user.has_group('pemesanan_atk.group_manager'):
                        raise AccessError(
                            "Hanya Manager ATK yang boleh menyetujui atau menolak transaksi.")
                    continue
                raise UserError(
                    "Perubahan status dari %s ke %s tidak diizinkan."
                    % (transaksi.state, target))
        return super(Transaksi, self).write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group('pemesanan_atk.group_manager'):
            if self.filtered(lambda r: r.state in ('approved', 'reject')):
                raise UserError(
                    "Transaksi yang sudah diproses tidak bisa dihapus. Hubungi Manager ATK.")
        return super(Transaksi, self).unlink()

    @api.multi
    def action_submit(self):
        return self.write({'state': 'rfa'})

    @api.multi
    def action_approve(self):
        return self.write({'state': 'approved'})

    @api.multi
    def action_reject(self):
        return self.write({'state': 'reject'})

    @api.multi
    def action_print_pdf(self):
        return self.env['report'].get_action(self, 'pemesanan_atk.my_report_transaksi')

    @api.multi
    def action_print_xlsx(self):
        return self.env['report'].get_action(self, 'pemesanan_atk.transaksi_report_xlsx')

    @api.depends('transaksi_line_ids.total_harga')
    def _compute_total_harga(self):
        for rec in self:
            rec.total_harga = sum(rec.transaksi_line_ids.mapped('total_harga'))


class BarangAtk(models.Model):
    _name = 'pemesanan_atk.barang_atk'
    _description = 'Barang ATK'
    _order = 'name'

    name = fields.Char(string='Nama Barang', required=True)
    stok_barang = fields.Integer(string='Stok', required=True)
    harga_barang = fields.Float(string='Harga', required=True)
    active = fields.Boolean(string='Active', default=True)


class TransaksiLine(models.Model):
    _name = 'pemesanan_atk.transaksi_line'
    _description = 'Rincian Transaksi ATK'

    transaksi_id = fields.Many2one(
        'pemesanan_atk.transaksi_barang', string='Transaksi', ondelete='cascade')
    barang_id = fields.Many2one('pemesanan_atk.barang_atk', string='Barang')
    jumlah = fields.Integer(string='Jumlah', required=True, default=1)
    total_harga = fields.Float(
        string='Total Harga', compute='_compute_total_harga', store=True)

    @api.constrains('barang_id', 'jumlah')
    def _check_jumlah(self):
        for line in self:
            if not line.barang_id:
                continue
            if line.jumlah > line.barang_id.stok_barang:
                raise ValidationError(
                    'Jumlah pemesanan %s melebihi stok barang yang tersedia.'
                    % line.barang_id.name)
            if line.jumlah <= 0:
                raise ValidationError("Jumlah harus lebih besar dari 0")

    @api.depends('barang_id.harga_barang', 'jumlah')
    def _compute_total_harga(self):
        for rec in self:
            rec.total_harga = rec.barang_id.harga_barang * rec.jumlah

    @api.onchange('barang_id')
    def _onchange_barang_id(self):
        if self.barang_id:
            self.jumlah = 1