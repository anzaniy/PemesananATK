# -*- coding: utf-8 -*-

from odoo import models, fields


class Department(models.Model):
    _name = 'pemesanan_atk.department'
    _description = 'Departemen'

    name = fields.Char(string='Nama Departemen', required=True)
    transaksi_ids = fields.One2many(
        'pemesanan_atk.transaksi_barang', 'department_id', string='Transaksi')
