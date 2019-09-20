# -*- coding: utf-8 -*-
{
    'name': "MLP",

    'summary': """
        MLP
        """,
    'description': """
        MLP
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
        'data/decomposicao_preco_data.xml',
        'data/decomposicao_localidade_data.xml',
        'data/tipo_garantia_data.xml',
        'data/garantidor_data.xml',
        'data/tipo_garantia_garantidor_data.xml',
        'views/operacao_mlp.xml',
        'views/res_partner_devedor.xml',
        'views/res_partner_garantidor.xml',
        'views/res_partner_solicitante.xml',
        'views/res_partner_mandatario.xml',
        'views/tipo_garantia.xml',
        'views/tipo_garantia_garantidor.xml',
        'views/menu.xml',
    ],
    'qweb': [
    ],
    'application': True,
}
