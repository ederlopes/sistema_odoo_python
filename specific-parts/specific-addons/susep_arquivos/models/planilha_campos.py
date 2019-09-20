# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PlanilhaCampos(models.Model):

    _name = 'susep.planilha_campos'
    _rec_name = 'mapeamento_id'
    _description = 'Relacionamento Planilha Campos'

    planilha_id = fields.Many2one(
        comodel_name='susep.planilha',
        string='Planilha'
    )

    mapeamento_id = fields.Many2one(
        string='Campos',
        comodel_name='susep.mapeamento',
    )

    sequence = fields.Integer(
        'Sequence',
        default=1,
        help="Used to order subtypes."
    )
