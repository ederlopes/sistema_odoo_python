# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Status(models.Model):
    _name = "status"
    _description = "Status serais do sistema."
    _rec_name = 'name'

    name = fields.Char(
        string='Status',
        required=True,
    )

    sigla = fields.Char(
        string='Sigla',
    )

    active = fields.Boolean(
        string='Ativo',
        required=True,
    )
