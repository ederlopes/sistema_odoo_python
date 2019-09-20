# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SetorAtividade(models.Model):

    _name = "setor.atividade"
    _description = "Setor de Atividade da Empresa"


    name = fields.Char(
        string='Nome',
        required=True,
    )

    linha_negocio_id = fields.Many2one(
        comodel_name='linha.negocio',
        string='Linha de negocio'
    )

    active = fields.Boolean(
        string='Ativo',
    )

    @api.multi
    def name_get(self):
        result = []

        for record in self:
            if len(record.name) > 100:
                name = "{} ...".format(record.name[:100])
            else:
                name = record.name

            result.append((record.id, name))

        return result