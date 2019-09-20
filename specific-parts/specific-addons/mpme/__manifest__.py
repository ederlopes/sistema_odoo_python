# -*- coding: utf-8 -*-
{
    'name': "MPME",

    'summary': """
        MPME
        """,
    'description': """
        MPME
    """,
    'author': "ABGF",
    'website': "http://www.abgf.gov.br",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['sce', ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/operacao_mpme.xml',
        'views/menu.xml',
    ],
    'qweb': [
    ],
    'application': True,
}
