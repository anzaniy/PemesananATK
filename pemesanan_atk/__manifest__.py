# -*- coding: utf-8 -*-
{
    'name': "Pemesanan ATK",

    'summary': """
        Permintaan alat tulis kantor dengan alur approval dan laporan PDF/Excel""",

    'description': """
Modul pemesanan ATK: master barang dan departemen, transaksi pemesanan dengan
alur draft - RFA - approved/reject, validasi stok, serta laporan PDF dan Excel.
    """,

    'author': "anzaniy",
    'website': "https://github.com/anzaniy/PemesananATK",
    'license': "LGPL-3",

    'category': 'Inventory',
    'version': '10.0.2.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'report_xlsx'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/department.xml',
        'views/barang.xml',
        'views/transaksi.xml',
        'wizard/wizard_view.xml',
        'report/report_view.xml',
        'report/print_transaksi.xml',
    ],

    'installable': True,
    'application': True,
}
