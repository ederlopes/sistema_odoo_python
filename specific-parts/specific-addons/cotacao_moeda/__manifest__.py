# -*- coding: utf-8 -*-
{
    'name': "Cotação Diária",

    'summary': """
        Cotação Diária
        """,
    'description': """
        Cotação Diária
    """,
    'author': "ABGF",
    'website': "http://www.abgf.gov.br",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/email_notificacao_cotacao.xml',
        'data/cron_cotacao_diaria.xml',
        'views/cotacao_diaria_view.xml',
        'views/menu.xml',
    ],
    'application': True,
}
