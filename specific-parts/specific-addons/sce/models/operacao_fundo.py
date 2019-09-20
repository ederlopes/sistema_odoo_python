# -*- coding: utf-8 -*-
from odoo import models, fields, api


class OperacaoFundo(models.Model):
    _name = "operacao.fundo"
    _rec_name = "fundo_id"
    _description = "Operação Fundo"

    operacao_id = fields.Many2one(
        comodel_name='operacao',
        string='Operação',
    )

    fundo_id = fields.Many2one(
        comodel_name='fundo',
        string='Fundo',
    )

    percent_utilizado = fields.Float(
        string="% utilizado do fundo",
        default=0.0,
    )

    saldo_suficiente = fields.Selection(
        string='Saldo suficiente',
        selection=[('sim', 'Sim'), ('nao', 'Não')],
    )

    valor_solicitado = fields.Float(
        string='Valor Solicitado',
    )

    taxa_cotacao = fields.Float(
        string='Taxa da cotação(d-1)',
    )

    valor_aprovacao = fields.Float(
        string='Valor para aprovação (R$)',
        compute='_compute_percent_utilizado',
        store=True,
    )

    @api.multi
    @api.depends('percent_utilizado', 'valor_solicitado', 'taxa_cotacao')
    @api.onchange('percent_utilizado', 'valor_solicitado', 'taxa_cotacao')
    def _compute_percent_utilizado(self):
        for obj in self:
            obj.valor_aprovacao = (obj.percent_utilizado/100)*(
                    obj.valor_solicitado*obj.taxa_cotacao)
