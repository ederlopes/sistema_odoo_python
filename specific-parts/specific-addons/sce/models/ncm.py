# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Ncm(models.Model):
    _name = 'ncm'

    name = fields.Char(
        string='Descrição da NCM',
    )

    numero = fields.Char(
        string='Número',
    )

    active = fields.Boolean(
        string='Ativo',
    )
