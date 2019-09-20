# -*- coding: utf-8 -*-

from odoo import models, fields, api

TIPO_CAMPO = [('N', 'NÚMERICO'), ('F', 'FLOAT'), ('C', 'CARACTER'),
              ('D', 'DATA')]
TROCAR_VALOR = [('sim', 'SIM'), ('nao', 'NÃO')]

class Mapeamento(models.Model):

    _name = 'susep.mapeamento'
    _description = 'Campos mapeados de cada tab do excel'

    name = fields.Char(
        string='Nome do Campo'
    )

    tipo_campo = fields.Selection(
        string=u'Tipo campo',
        selection=TIPO_CAMPO,
    )

    tamanho_campo = fields.Char(
        string='Tamanho do campo'
    )

    formato1 = fields.Char(
        string='Formato do Campo 1'
    )

    formato2 = fields.Char(
        string='Formato do Campo 2'
    )

    trocar_valor = fields.Selection(
        string='Trocar Valor',
        selection=TROCAR_VALOR,
        default=TROCAR_VALOR[1][0]
    )


