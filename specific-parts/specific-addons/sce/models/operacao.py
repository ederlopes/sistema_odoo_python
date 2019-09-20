# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


TIPO_SOLICITANTE = [('exportador', 'Exportador'),
                    ('instituicao_financeira', 'Instituição Financeira'),
                    ('outros', 'Outros')]


class OperacaoAtributos(models.AbstractModel):
    _name = 'operacao.atributos'
    _description = 'Operações'
    _rec_name = 'nu_oper_interno'
    _inherit = ['mail.thread']

    nu_oper_interno = fields.Char(
        string='Número da Operação',
    )

    nu_oper_susep = fields.Char(
        string='Número da Operação na SUSEP',
    )

    exportador_id = fields.Many2one(
        comodel_name='exportador',
        string='Exportador',
    )

    importador_id = fields.Many2one(
        comodel_name='importador',
        string='Importador',
    )

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='País',
    )

    country_ctrl_pais_id = fields.Many2one(
        comodel_name='res.country',
        string='País',
        related='country_id',
    )

    exportador_linha_negocio_id = fields.Many2one(
        comodel_name='exportador.linha.negocio',
        string='Modalidade',
    )

    linha_negocio_id = fields.Many2one(
        comodel_name='linha.negocio',
        related='exportador_linha_negocio_id.linha_negocio_id',
        string='Linha de Negócio',
    )

    state = fields.Many2one(
        comodel_name='status',
        string='Status',
    )

    state_sigla = fields.Char(
        related='state.sigla'
    )

    moeda = fields.Selection(
        selection=[('usd', 'USD'),
                   ('eur', 'EUR'), ],
        string=u'Moeda da operação',
    )

    moeda_ctrl_pais = fields.Selection(
        selection=[('usd', 'USD'),
                   ('eur', 'EUR'), ],
        string=u'Moeda da operação',
        related='moeda',
    )

    valor_solicitado = fields.Float(
        string=u'Valor Solicitado',
    )

    valor_solicitado_ctrl_pais = fields.Float(
        string=u'Valor Solicitado',
        related='valor_solicitado',
    )

    modalidade_escolhida = fields.Char(
        string='Modalidade Escolhida',
    )

    parecer_controle_pais = fields.Text(
        string="Parecer Controle País",
    )

    saldo_suficiente = fields.Selection(
        string='Saldo Suficiente',
        selection=[('sim', 'Sim'), ('nao', 'Não')],
    )

    setor_atividade_ids = fields.Many2many(
        comodel_name='setor.atividade',
        string='Setor de Atividade'
    )

    fundo_principal_id = fields.Many2one(
        comodel_name='fundo',
        string='Fundo Principal',
    )

    operacao_fundo_ids = fields.Many2many(
        comodel_name='operacao.fundo',
        string='Controle de Capital',
    )

    taxa_cotacao = fields.Float(
        string='Taxa da cotação(d-1)',
        digits=(2, 5),
    )

    vl_solicitado_cotacao = fields.Float(
        string="Valor Total em R$",
        compute='_compute_vl_solicitado_cotacao',
    )

    @api.depends('taxa_cotacao', 'valor_solicitado')
    def _compute_vl_solicitado_cotacao(self):
        self.vl_solicitado_cotacao = self.valor_solicitado*self.taxa_cotacao


class Operacao(models.Model):
    _name = 'operacao'
    _description = 'Operação'
    _inherit = ['operacao.atributos']

    @api.multi
    def write(self, vals):
        if 'operacao_fundo_ids' in vals:
            try:
                tl_percent = sum([self.operacao_fundo_ids.browse(
                    of[1]).percent_utilizado if not of[2] else of[2][
                    'percent_utilizado'] for of in vals['operacao_fundo_ids']])

                if tl_percent != 0 and tl_percent != 100:
                    raise UserError('O somatório dos fundos precisa ser 100%')
            except:
                pass

        super(Operacao, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(Operacao, self).create(vals)
        partner_analista_ids = self.env['res.groups'].search(
            [('name', '=', 'Analista')]).users.mapped('partner_id')

        res.message_partner_ids = partner_analista_ids.mapped('id')

        return res

    def lista_state(self):
        status_l_ids = self.linha_negocio_id.mapped('status_linha_negocio_ids')
        status_ids = status_l_ids.sorted(
            lambda r: r.ordem).mapped('status_id').mapped('id')

        return status_ids

    @api.onchange('linha_negocio_id')
    def _onchange_exportador_linha_negocio_id(self):
        if self.linha_negocio_id:
            status_ids = self.lista_state()
            res = {'domain': {
                'state': "[('id', 'in', {})]".format(str(status_ids))},
                'value': {'state': status_ids[0]}}
        else:
            res = {'domain': {'state': "[(id, 'in', [])]"}}

        return res

    @api.onchange('operacao_fundo_ids', 'taxa_cotacao')
    def _onchange_operacao_fundo_ids(self):
        for of in self.operacao_fundo_ids:
            of.valor_solicitado = self.valor_solicitado
            of.taxa_cotacao = self.taxa_cotacao

        self.fundo_principal_id = self.operacao_fundo_ids.sorted(
            key=lambda r: r.percent_utilizado)[-1:].fundo_id

        tl_percent = sum(self.operacao_fundo_ids.mapped('percent_utilizado'))
        if tl_percent > 100:
            raise UserError('O somatório da porcentagem dos fundos '
                            'não pode ser maior que 100%')

    @api.onchange('state')
    def _onchange_state(self):
        if self.linha_negocio_id:
            p_state = self.lista_state()[0]
            if self.env.user.has_group('sce.group_exportador') \
                    and self.state.id != p_state:
                raise UserError('Somente o funcionário da '
                                'ABGF pode alterar o status.')

    @api.onchange('operacao_fundo_ids', 'taxa_cotacao')
    def _onchange_operacao_fundo_ids(self):
        for of in self.operacao_fundo_ids:
            of.valor_solicitado = self.valor_solicitado
            of.taxa_cotacao = self.taxa_cotacao
            of.valor_aprovacao = (of.percent_utilizado/100)*(
                    self.valor_solicitado*self.taxa_cotacao)

    @api.multi
    def enviar_operacao(self):
        for record in self:
            domain = ('linha_negocio_id', '=', self.linha_negocio_id.id)
            ordem = self.env['status.linha.negocio'].search(
                [('status_id.sigla', '=', record.state.sigla), domain]).ordem+1
            proximo = self.env['status.linha.negocio'].search(
                [('ordem', '=', ordem), domain]).status_id

            record.state = proximo
            self.notifica_nova_operacao()

            fundo_ids = self.env['fundo'].search([])
            # Cria linhas para porcentagem dos fundos ativos
            values = list()
            for fundo_id in fundo_ids:
                op_fundo_id = self.env['operacao.fundo'].create(
                    {'operacao_id': record.operacao_id.id,
                     'fundo_id': fundo_id.id, 'percent_utilizado': 0.0})
                values.append(op_fundo_id.id)
            record.operacao_fundo_ids = [(6, 0, values)]

    def notifica_nova_operacao(self):
        template = self.env.ref('sce.email_notificacao_envio_operacao_analista')
        linha_modalidade = self.exportador_linha_negocio_id.name_get()[0][1]
        body = template.body_html
        body = body.replace('--exportador--', self.exportador_id.name)
        body = body.replace('--importador--', self.importador_id.name)
        body = body.replace('--modalidade--', linha_modalidade)
        body = body.replace('--pais--', self.country_id.name)
        url_padrao = self.env['ir.config_parameter'].sudo()\
            .get_param('web.base.url')
        url = '{}/web#id={}&model=operacao&view_type=form'.format(
            url_padrao, self.id)
        url_img = '{}/sce/static/src/img/sce_logo.png'.format(url_padrao)
        body = body.replace('--url--', url)
        body = body.replace('--url_img--', url_img)
        template.body_html = body
        grupos = ['Analista', 'Gerente']

        return self.enviar_email(template=template, grupos=grupos)

    def prepara_email(self, template, grupos):
        if template:
            user_ids = self.env['res.groups'].sudo().search(
                [('name', 'in', grupos)]).mapped('users')
            emails = ';'.join(user_ids.mapped('email'))
            partner_ids = user_ids.mapped('id')
            mail_values = {'subject': template.subject,
                           'body_html': template.body_html,
                           'email_from': template.email_from,
                           'email_to': emails,
                           'partner_ids': partner_ids}

            return mail_values

    def enviar_email(self, template, grupos):
        mail_values = self.prepara_email(template=template, grupos=grupos)

        return self.env['mail.mail'].create(mail_values).send()
