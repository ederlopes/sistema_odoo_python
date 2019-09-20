# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ExportadorValidacao(models.Model):
    _name = "exportador.validacao"
    _description = "Exportador validação"
    _rec_name = 'validacao_id'
    _sql_constraints = [
        ('partner_exportador_validacao_unique',
         'unique(exportador_id, validacao_id)',
         'Essa validação ja existe para esse exportador.')]

    exportador_id = fields.Many2one(
        string='Exportador',
        comodel_name='exportador',
        ondelete='cascade',
        required=True,
    )

    validacao_id = fields.Many2one(
        string='Validação',
        comodel_name='validacao',
    )

    validacao_name = fields.Char(
        string='Atividade a fazer',
        related="validacao_id.name"
    )

    validacao_url = fields.Char(
        string='Url do site a verificar',
        related="validacao_id.url"
    )

    concluido = fields.Boolean(
        string='Concluido?',
    )

    @api.model
    def create(self, vals):
        result = self.search_count(
            [('exportador_id', '=', vals.get('exportador_id')),
             ('validacao_id', '=', vals.get('validacao_id'))])

        if result == 0:
            return super(ExportadorValidacao, self).create(vals)
