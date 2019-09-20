# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Fundo(models.Model):
    _name = "fundo"
    _rec_name = "name"
    _description = "Fundo"

    name = fields.Char(
        string='Nome',
    )

    active = fields.Boolean(default=True)
