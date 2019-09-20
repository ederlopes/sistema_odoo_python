# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NuturezaJuridica(models.Model):
    _name = "natureza.juridica"
    _description = "Natureza Juridica"

    name = fields.Char(
        string='Natureza Juridica',
        required=True,
    )

    active = fields.Boolean(
        string='Ativo',
    )

    natureza_risco_ids = fields.One2many(
        comodel_name='natureza.risco',
        inverse_name='natureza_juridica_id',
        string='Natureza Risco'
    )
