# -*- coding: utf-8 -*-
from odoo import models, fields, api


SIM_NAO = [('sim', 'Sim'), ('nao', 'Não')]


class OperacaoMpme(models.Model):
    _inherits = {'operacao': 'operacao_id'}
    _inherit = 'operacao'
    _name = 'operacao.mpme'
    _description = 'Operação MPME'
    _rec_name = 'id'

    operacao_id = fields.Many2one(
        comodel_name='operacao',
        string='Operação',
        ondelete="cascade",
        required=True,
    )

    natureza_juridica_id = fields.Many2one(
        comodel_name='natureza.juridica',
        string='Natureza Jurídica',
    )

    natureza_risco_id = fields.Many2one(
        comodel_name='natureza.risco',
        string='Natureza do Risco',
    )

    flag_demonstrativo = fields.Boolean(
        string='A fim de que possamos dar continuidade à analise da operação, '
               'solicitamos enviar, se possível com brevidade, os '
               'demonstrativos financeiros dos últimos 3 (três) anos.',
    )

    first_exp_empresa = fields.Selection(
        selection=SIM_NAO,
        string=u'É a primeira exportação da empresa?',
    )

    first_exp_prod = fields.Selection(
        selection=SIM_NAO,
        string=u'É a primeira exportação deste produto?',
    )

    first_exp_pais = fields.Selection(
        selection=SIM_NAO,
        string=u'É a primeira exportação para este país?',
    )

    first_exp_sce = fields.Selection(
        selection=SIM_NAO,
        string=u'É a primeira exportação com o uso do SCE?',
    )

    setor_atividade_ids = fields.Many2many(
        comodel_name='setor.atividade',
        string='Setor de Atividade'
    )

    total_valor_operacoes = fields.Float(
        string='Total operacao',
        compute='total_operacao',
        store=True,
    )

    @api.multi
    def write(self, vals):
        super(OperacaoMpme, self).write(vals)

    def total_operacao(self):
        preco = sum(self.env['operacao.mpme'].search([]).mapped(
            'valor_solicitado'))
        self.total_valor_operacoes = preco
