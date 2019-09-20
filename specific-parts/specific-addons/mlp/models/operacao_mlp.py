# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.sce.constants import *
from odoo.exceptions import Warning


TIPO_SOLICITANTE = [('exportador', 'Exportador'),
                    ('instituicao_financeira', 'Instituição Financeira'),
                    ('outros', 'Outros')]


class OperacaoMLP(models.Model):
    _inherits = {'operacao': 'operacao_id'}
    _inherit = 'operacao'
    _name = 'operacao.mlp'

    operacao_id = fields.Many2one(
        comodel_name='operacao',
        string='Operação',
        ondelete="cascade",
        required=True,
    )

    tipo_solicitante = fields.Selection(
        string=u'Tipo de Solicitante',
        selection=TIPO_SOLICITANTE,
        required=True,
    )

    instituicao_financeira_id = fields.Many2one(
        comodel_name='instituicao.financeira',
        string='Instituição Financeira',
    )

    solicitante_id = fields.Many2one(
        comodel_name='res.partner',
        string='Solicitante',
    )

    devedor_id = fields.Many2one(
        comodel_name='devedor',
        string='Devedor',
    )

    mandatario_id = fields.Many2one(
        comodel_name='mandatario',
        string='Mandatário',
    )

    tipo_garantia_id = fields.Many2one(
        comodel_name='tipo.garantia',
        string='Tipo de Garantia',
    )

    garantidor_id = fields.Many2one(
        comodel_name='tipo.garantia.garantidor',
        inverse_name='garantidor_id',
        string='Garantidor',
        ondelete='cascade',
    )

    permite_criar_garantidor = fields.Boolean(
        string='Permitir criar garantidor',
        related='tipo_garantia_id.permite_criar_garantidor',
    )

    agencia_id = fields.Many2one(
        comodel_name='agencia',
        string='Agência',
    )

    solicitante_name = fields.Char(
        string='Solicitante',
        related='solicitante_id.name',
    )

    devedor_como_importador_name = fields.Char(
        string='Devedor',
        related='importador_id.name',
    )

    solicitante_cpf_cnpj = fields.Char(
        string='CNPJ',
        related='solicitante_id.cpf_cnpj',
    )

    copiar_dados_importador = fields.Boolean(
        string='O devedor possui os mesmos dados do importador'
    )

    objeto_exportacao = fields.Html('Objeto da exportação')

    icoterm = fields.Char(
        string='Icoterm',
    )

    contato = fields.Char(
        string='Contato',
    )

    contato_email = fields.Char(
        string='E-mail',
    )

    contato_telefone = fields.Char(
        string='Telefone',
    )

    contato_cargo = fields.Char(
        string='Cargo',
    )

    natureza_juridica_id = fields.Many2one(
        comodel_name='natureza.juridica',
        string='Natureza Juridica'
    )

    operacao_mercadoria_ids = fields.One2many(
        comodel_name='operacao.mercadoria',
        inverse_name='operacao_id',
        string='Mercadorias'
    )

    total_valor_operacoes = fields.Float(
        string='Total operacao',
        compute='total_operacao',
        store=True,
    )

    def total_operacao(self):
        preco = sum(self.env['operacao.mlp'].search([]).mapped(
            'valor_solicitado'))
        self.total_valor_operacoes = preco

    def _default_dec_precos(self):

        preco = self.env['decomposicao.preco'].search([('active', '=', True)])
        localidade = self.env['decomposicao.localidade'].search(
            [('active', '=', True)])

        return [
            (0, 0, {
                'decomposicao_preco_id': p.id,
                'decomposicao_localidade_id': l.id,
                'valor_brasileiro': 0,
                'valor_estrangeiro': 0,
                'valor_local': 0,
            })
            for p in preco
            for l in localidade
        ]

    precos_ids = fields.Many2many(
        'operacaomlp.depomposicao.preco',
        string='Descrição',
        default=_default_dec_precos)

    @api.model
    def create(self, vals):
        if vals['copiar_dados_importador']:
            id_partner = self.env['importador'].\
                browse(vals['importador_id']).partner_id
            vals['devedor_id'] = self.env['devedor'].create({
                'partner_id': id_partner.id
            }).id

        return super(OperacaoMLP, self).create(vals)

    @api.multi
    def write(self, vals):
        # linha_negocio_id = self.env.ref("sce.linha_negocio_mlp").id
        # state = self.env['status'].search([('sigla', '=',
        #                                     'aguardando_envio'),
        #                                    ('linha_negocio_id', '=',
        #                                     linha_negocio_id)])
        # vals['state'] = vals['state'] if 'state' in vals and vals['state'] \
        #                                  is not False else state.id

        return super(OperacaoMLP, self).write(vals)

    @api.onchange('exportador_id')
    def _onchange_exportador_id(self):
        self.exportador_linha_negocio_id = False
        if self.tipo_solicitante == 'exportador':
            self.solicitante_id = self.exportador_id.partner_id
            res = {'value': {
                'solicitante_id': self.exportador_id.partner_id.id,
                'exportador_linha_negocio_id': False},
                'domain': {'solicitante_id': "[('id', 'in', [{}])]".format(
                    self.exportador_id.partner_id.id)}}
        else:
            res = {'value': {'exportador_linha_negocio_id': False}}
        return res

    @api.onchange('instituicao_financeira_id')
    def _onchange_instituicao_financeira(self):
        if self.tipo_solicitante == 'instituicao_financeira':
            self.solicitante_id = self.instituicao_financeira_id.partner_id
            res = {'value': {
                'solicitante_id': self.instituicao_financeira_id.partner_id.id},
                'domain': {'solicitante_id': "[('id', 'in', [{}])]".format(
                    self.instituicao_financeira_id.partner_id.id)}}

            return res

    @api.onchange('tipo_solicitante')
    def _onchange_tipo_solicitante(self):
        res = dict()
        if self.tipo_solicitante == 'exportador':
            self.solicitante_id = self.exportador_id.partner_id
            res = {'value': {
                'solicitante_id': self.exportador_id.partner_id.id},
                'domain': {'solicitante_id': "[('id', 'in', [{}])]".format(
                    self.exportador_id.partner_id.id)}}

        if self.tipo_solicitante == 'instituicao_financeira':
            self.solicitante_id = self.instituicao_financeira_id.partner_id
            res = {'value': {
                'solicitante_id': self.instituicao_financeira_id.partner_id.id},
                'domain': {'solicitante_id': "[('id', 'in', [{}])]".format(
                    self.instituicao_financeira_id.partner_id.id)}}

        if self.tipo_solicitante == 'outros':
            self.solicitante_id = False
            res = {'value': {'solicitante_id': False},
                   'domain': {
                       'solicitante_id': "[('is_solicitante', '=', True)]"}}

        return res

    @api.onchange('instituicao_financeira_id')
    def _onchange_instituicao_financeira_id(self):
        self.agencia_id = False
        res = {'value': {'agencia_id': False}}
        return res

    @api.onchange('tipo_garantia_id')
    def _onchange_tipo_garantia_id(self):
        res = dict()
        if self.tipo_garantia_id:
            if self.tipo_garantia_id.permite_criar_garantidor == False:
                self.garantidor_id = False
                res = {'value': {'garantidor_id': 1}}
            else:
                self.garantidor_id = False
                res = {'value': {'garantidor_id': 2}}
            return res
