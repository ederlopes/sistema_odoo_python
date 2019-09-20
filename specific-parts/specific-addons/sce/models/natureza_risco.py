# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NaturezaRisco(models.Model):

    _name = "natureza.risco"
    _description = "Natureza Risco"

    name = fields.Char(
        string='Nome',
        required=True,
    )

    active = fields.Boolean(
        string='Ativo',
    )

    natureza_juridica_id = fields.Many2one(
        comodel_name='natureza.juridica',
        string='Natureza Juridica'
    )
