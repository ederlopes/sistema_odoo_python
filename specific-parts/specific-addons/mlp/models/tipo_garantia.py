# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TipoGarantia(models.Model):

    _name = "tipo.garantia"
    _description = "Tipo de Garantia"

    name = fields.Char(
        string='Nome',
        required=True,
    )

    permite_criar_garantidor = fields.Boolean(
        string='Permitir criar garantidor',
    )

    active = fields.Boolean(
        string='Ativo',
    )

