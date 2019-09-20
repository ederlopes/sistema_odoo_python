# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ValoresPaises(models.Model):
    _name = "valores.paises"
    _description = "Validação de atividades"

    active = fields.Boolean(
        string='Ativo',
    )

    pais_id = fields.Many2one(
        comodel_name='res.country',
        string="Pais",
    )

    risco = fields.Integer(
        string='Risco'
    )

    pres_credito = fields.Integer(
        string='PRES.CRÉD.'
    )

    ibnr = fields.Float(
        digits=(15, 2),
        string='IBNR',
    )

    pip = fields.Float(
        digits=(15, 2),
        string='PIP',
    )

    lim_credito = fields.Float(
        digits=(15, 2),
        string='Limite de crédito',
    )

    import_mundo = fields.Float(
        digits=(15, 2),
        string='Import. Mundo',
    )

    import_brasil = fields.Float(
        digits=(15, 2),
        string='Import. Brasil',
    )

    data_vigencia = fields.Datetime(
        string='Data de Vigencia'
    )














