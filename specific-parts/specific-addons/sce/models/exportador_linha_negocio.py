# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ExportadorLinhaNegocio(models.Model):
    _name = "exportador.linha.negocio"
    _description = "Exportador, Linha de Negócio e Modalidade"
    _rec_name = 'modalidade_id'
    _sql_constraints = [
        ('exportador_linha_negocio_modalidade_unique',
         'unique(exportador_id, linha_negocio_id, modalidade_id, '
         'tipo_financiamento_id)',
         'A linha de negócio e modalidade precisam únicas para esta empresa.')]

    active = fields.Boolean(
        string=u'Status',
        default=False,
    )

    exportador_id = fields.Many2one(
        string='Exportador',
        comodel_name='exportador',
        required=True,
    )

    linha_negocio_id = fields.Many2one(
        string='Sigla',
        comodel_name='linha.negocio',
    )

    modalidade_id = fields.Many2one(
        comodel_name='modalidade',
        string='Modalidades',
    )

    tipo_financiamento_id = fields.Many2one(
        comodel_name='tipo.financiamento',
        string='Tipo de Financiamento',
    )

    @api.multi
    def write(self, vals):
        vals['active'] = vals.get('active') if 'active' in vals else False
        super(ExportadorLinhaNegocio, self).write(vals)

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append(eval("({},'{} - {}')".format(
                record.id, record.linha_negocio_id.sigla,
                record.modalidade_id.sigla)))

        return res

    @api.multi
    def toggle_active(self):
        return super(ExportadorLinhaNegocio, self).toggle_active()
