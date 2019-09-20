# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TipoGarantiaGarantidor(models.Model):

    _name = "tipo.garantia.garantidor"
    _description = "Tipo de garantia relacionado com garantidor"
    _rec_name = 'garantidor_id'

    tipo_garantia_id = fields.Many2one(
        comodel_name='tipo.garantia',
        string='Tipo de garantia'
    )

    garantidor_id = fields.Many2one(
        comodel_name='garantidor',
        string='Garantidor'
    )

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append(eval("({},'{}')".format(
                record.id, record.garantidor_id.name)))
        return res