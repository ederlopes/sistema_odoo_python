# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

ANO_INFORMACOES = [(y, y) for y in range(int(datetime.now().year) - 2,
                                         int(datetime.now().year) + 1)]


class ResPartner(models.Model):
    _inherit = "res.partner"

    _sql_constraints = []

    cpf_cnpj = fields.Char(
        string='CPF_CNPJ',
    )

    is_solicitante = fields.Boolean(
        string=u'Empresa Solicitante',
        default=False,
    )

    @api.multi
    def edit_my_partner_save(self):
        """
        Simple edit my partner in right corner.
        Action triggered in wizard "simple edit partner"
        """
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }
