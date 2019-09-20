# -*- coding: utf-8 -*-
{
    'name': "Susep arquivos",

    'summary': """
        Susep arquivos
        """,
    'description': """
        SCE
    """,
    'author': "ABGF",
    'website': "http://www.abgf.gov.br",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/quadros.xml',
        'data/planilha.xml',
        'data/campos_mapeamento.xml',
        'data/planilha_campos.xml',
        'views/principal_view.xml',
        'views/quadro_view.xml',
        'views/planilha_view.xml',
        'views/mapeamento_view.xml',
        'views/planilha_campos_view.xml',
        'views/menu.xml',
    ],
    'application': True,
}
