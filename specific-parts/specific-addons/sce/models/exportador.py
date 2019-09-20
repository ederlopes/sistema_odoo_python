# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning
from pycpfcnpj import cpfcnpj
from datetime import datetime
from odoo.addons.sce.constants import *

ANO_INFORMACOES = [(y, y) for y in range(int(datetime.now().year) - 2,
                                         int(datetime.now().year) + 1)]


class Exportador(models.Model):
    _inherits = {'res.partner': 'partner_id'}
    _name = 'exportador'

    _sql_constraints = []

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete="cascade",
        required=True,
    )

    funcionario_exportador_ids = fields.One2many(
        comodel_name='funcionario.exportador',
        inverse_name='exportador_id',
        string='Funcionários',
        ondelete='cascade',
    )

    bank_ids = fields.Many2many(
        comodel_name='res.bank',
        string='Instituições Financeiras',
    )

    socio_ids = fields.One2many(
        comodel_name='socio',
        inverse_name='exportador_id',
        string='Sócios',
    )

    total_portentagem_socio = fields.Float(
        string='Total porcentagem',
        compute='total_porcentagem_socio',
        store=True,
    )

    exportador_validacao_ids = fields.One2many(
        comodel_name='exportador.validacao',
        inverse_name='exportador_id',
        string='Validação',
    )

    exportador_linha_negocio_ids = fields.One2many(
        comodel_name='exportador.linha.negocio',
        inverse_name='exportador_id',
        string='Linhas de Negócios',
        ondelete='cascade',
        context={'active_test': False},
    )

    simples_nacional = fields.Selection(
        string='Simples Nacional',
        selection=SIM_NAO,
    )

    razao_social = fields.Char(
        string='Razão Social',
    )

    inscricao_estadual = fields.Char(
        string='Inscrição Estadual',
    )

    capital_social = fields.Float(
        string='Capital Social',
    )

    n_funcionarios = fields.Integer(
        string='N° de funcionários',
    )

    participou_evento = fields.Selection(
        string='Participou de algum evento de divulgação do SCE/MPME?',
        selection=SIM_NAO,
    )

    como_ficou_sabendo = fields.Selection(
        string='Como ficou sabendo do SCE/MPME?',
        selection=COMO_FICOU_SABENDO,
    )

    tempo_existencia = fields.Selection(
        string='Tempo de existência',
        selection=TEMPO_EXISTENCIA,
    )

    ano_informacoes = fields.Selection(
        string='Ano das informações',
        selection=ANO_INFORMACOES,
    )

    fat_bruto_anual = fields.Float(
        string='Faturamento Bruto Anual',
    )

    val_exportacao_anual = fields.Float(
        string='Valor de Exportação Anual',
    )

    dre = fields.Binary(string='DRE')

    comprovante_exportacoes = fields.Binary(
        string='Comprovante de Exportações')

    modalidades_escolhidas = fields.Char(
        string='Modalidades Escolhidas',
        default='m',
    )

    data_recomendacao = fields.Datetime(string='Data da recomendação',
                                        default=fields.Datetime.now)

    parecer_tecnico = fields.Html('Parecer Tecnico')

    state = fields.Selection([
        ('rascunho', 'Rascunho'),
        ('enviado', 'Enviado'),
        ('em_analise', 'Em Analise'),
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
    ], default='rascunho')

    @api.multi
    def _declaracao_conformidade_arq(self):
        domain = [('tipo_arquivo', '=', 'DECLARACAO_CONFORMIDADE_MPME')]
        template_id = self.env['template.arquivo'].search(
            domain)

        return "<p><a href='{}' " \
               "download class='btn btn-primary'>" \
               "<i class='fa fa-download'></i> {} </a></p>" \
               "<div class='alert alert-info " \
               "o_form_header' role='alert'>" \
               "<strong>{}</strong></div>".format(
                template_id.attachment_id.local_url,
                template_id.name,
                template_id.disclaimer)

    declaracao_conformidade_arq = fields.Html(
        default=_declaracao_conformidade_arq
    )

    declaracao_conformidade_assinado = fields.Binary(
        string='Declaração de Conformidade Assinada',
    )

    nome_declaracao_conformidade_assinado = fields.Char(
        string="Nome do Arquivo",
    )

    @api.multi
    def _declaracao_anti_corrupcao_arq(self):
        domain = [('tipo_arquivo', '=', 'DECLARACAO_ANTI_CORRUPCAO_MPME')]
        template_id = self.env['template.arquivo'].search(
            domain)

        return "<p><a href='{}' " \
               "download class='btn btn-primary'>" \
               "<i class='fa fa-download'></i> {} </a></p>" \
               "<div class='alert alert-info " \
               "o_form_header' role='alert'>" \
               "<strong>{}</strong></div>".format(
            template_id.attachment_id.local_url,
            template_id.name,
            template_id.disclaimer)

    declaracao_ant_corrupcao_arq = fields.Html(
        default=_declaracao_anti_corrupcao_arq
    )

    declaracao_ant_corrupcao_ass = fields.Binary(
        string='Declaração de Anti Corrupção',
    )

    nome_ant_corrupcao_assinado = fields.Char(
        string="Nome do Arquivo",
    )

    @api.multi
    def unlink(self):
        for record in self:
            if record.parent_id.id != record.env.user.partner_id.id \
                    and record.env.user.partner_id.name != 'OdooBot':
                raise Warning(u'Somente o Contato principal pode deletar '
                              u'a empresa.')

            return super(Exportador, record).unlink()

    modalidades_escolhidas = fields.Char(
        string='modalidades escolhidas',
        default='m'
    )

    @api.model
    def create(self, vals):
        vals['parent_id'] = self.env.user.partner_id.id
        vals['active'] = False
        if not cpfcnpj.validate(vals['cpf_cnpj']):
            raise Warning(u'CNPJ invalido.')
        else:
            if self.env['exportador'].search([('cpf_cnpj', '=',
                                               vals['cpf_cnpj'])
                                              ]).id:
                raise Warning(u'CNPJ já cadastrado.')

        res = super(Exportador, self).create(vals)
        # Vincula o usuário que criou ao grupo de funcionários
        vals = {'funcionario_id': self.env.user.partner_id.id,
                'exportador_id': res.id, }
        res.funcionario_exportador_ids.create(vals)

        return res

    @api.multi
    def write(self, vals):
        '''

        :param vals:
        :return:
        '''
        # Verifica se o CNPJ é válido
        if 'cpf_cnpj' in vals and self.is_company:
            if not cpfcnpj.validate(vals['cpf_cnpj']):
                raise Warning(u'CNPJ invalido.')

        if self.env.user.has_group('sce.group_exportador'):
            if self.state != 'rascunho':
                campos_permitidos = ['exportador_linha_negocio_ids']
                result = all(elem in campos_permitidos
                             for elem in list(vals.keys()))
                if result:
                    vals['state'] = 'rascunho'
                    res = super(Exportador, self).sudo().write(vals)
                    self.enviar_cadastro()

                    return res

        return super(Exportador, self).write(vals)

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

    @api.multi
    @api.depends('socio_ids')
    def total_porcentagem_socio(self):
        for record in self:
            if record.socio_ids:
                record.total_portentagem_socio = \
                    sum(record.socio_ids.mapped('percentual'))
                if record.total_portentagem_socio != 100:
                    raise Warning(u'A soma do percentual dos sócios deve ser '
                                  u'igual a 100%')

    @api.multi
    def enviar_cadastro(self):
        ln_ids = self.exportador_linha_negocio_ids.mapped('modalidade_id')
        if not len(ln_ids):
            raise Warning(u'Você precisa cadastrar uma linha de '
                          u'negocio antes de enviar sua empresa para analise!')
        elif not len(self.socio_ids):
            raise Warning(u'Você precisa cadastrar ao menos 1 socio '
                          u'antes de enviar sua empresa para analise!')
        else:
            self.notifica_novo_exportador_analise()
            self.write({'state': 'enviado'})

    def prepara_email(self, template, grupos):
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
        mail_values = self.prepara_email(template=template, grupos=grupos,)

        return self.env['mail.mail'].create(mail_values).send()

    def notifica_novo_exportador_analise(self):
        template = self.env.ref(
            'sce.email_notificacao_exportador_enviado_analise')
        body = template.body_html
        body = body.replace('--analista--', self.name)
        body = body.replace('--exportador--', self.name)
        url = self.env['ir.config_parameter'].sudo() \
            .get_param('web.base.url')
        url_img = '{}/sce/static/src/img/sce_logo.png'.format(url)
        body = body.replace('--url--', url)
        body = body.replace('--url_img--', url_img)
        template.body_html = body
        grupos = ['Analista', 'Gerente']

        return self.enviar_email(template=template, grupos=grupos)
