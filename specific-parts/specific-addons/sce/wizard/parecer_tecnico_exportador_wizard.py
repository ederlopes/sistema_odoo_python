# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning

class ParecerTecnicoExportadorWizard(models.TransientModel):
    _name = "parecer.tecnico.exportador.wizard"
    _description = "Wizard do parecer tecnico do exportador"
    _inherit = 'mail.thread'

    data_recomendacao = fields.Datetime(
        string='Data da recomendação',
        default=fields.Datetime.now,
        required=True,
    )

    parecer_tecnico = fields.Html('Parecer Tecnico', required=True, )

    def salvar_parecer(self, exportador_id):
        exportador_id.data_recomendacao = self.data_recomendacao
        exportador_id.parecer_tecnico = self.parecer_tecnico

        return True

    @api.multi
    def aprovar(self):
        active_ids = self.env.context['active_ids'][0]
        exportador_id = self.env['exportador'].browse(active_ids)
        validacoes = exportador_id.exportador_validacao_ids.mapped('concluido')
        linha_negocio = exportador_id.exportador_linha_negocio_ids.\
            mapped('active')
        if not all(validacoes):
            raise Warning(u'Existe validações de atividades pendentes.')
        elif not any(linha_negocio):
            raise Warning(u'Você'
                          u' precisa aprovar ao menos uma linha de negocio.')
        else:
            if self.salvar_parecer(exportador_id):
                exportador_id.write({
                    'state': 'aprovado'
                })
                self.notifica_exportador_aprovado()
                exportador_id.toggle_active()

    @api.multi
    def reprovar(self):
        active_ids = self.env.context['active_ids'][0]
        exportador_id = self.env['exportador'].browse(active_ids)
        if self.salvar_parecer(exportador_id):
            exportador_id.write({
                'state': 'reprovado'
            })
            exportador_id.active = False
            self.notifica_exportador_recusado()

    def prepara_email(self, template, email_exportador):
        if template:
            mail_values = {'subject': template.subject,
                           'body_html': template.body_html,
                           'email_from': template.email_from,
                           'email_to': email_exportador,
                           }
        return mail_values

    def enviar_email(self, template, email_exportador):
        mail_values = self.prepara_email(
            template=template,
            email_exportador=email_exportador,
        )

        return self.env['mail.mail'].create(mail_values).send()

    def notifica_exportador_aprovado(self):
        active_ids = self.env.context['active_ids'][0]
        exportador_id = self.env['exportador'].browse(active_ids)
        template = self.env.ref(
            'sce.email_notificacao_aprovar_exportador')
        body = template.body_html
        body = body.replace('--exportador--', exportador_id.name)
        body = body.replace('--status--', 'aprovado')
        url = self.env['ir.config_parameter'].sudo() \
            .get_param('web.base.url')
        url_img = '{}/sce/static/src/img/sce_logo.png'.format(url)
        body = body.replace('--url--', url)
        body = body.replace('--url_img--', url_img)
        template.body_html = body
        email_exp = exportador_id.email

        return self.enviar_email(
            template=template, email_exportador=email_exp
        )

    def notifica_exportador_recusado(self):
        active_ids = self.env.context['active_ids'][0]
        exportador_id = self.env['exportador'].browse(active_ids)
        template = self.env.ref(
            'sce.email_notificacao_recusado_exportador')
        body = template.body_html
        body = body.replace('--exportador--', exportador_id.name)
        url = self.env['ir.config_parameter'].sudo() \
            .get_param('web.base.url')
        url_img = '{}/sce/static/src/img/sce_logo.png'.format(url)
        body = body.replace('--url--', url)
        body = body.replace('--url_img--', url_img)
        template.body_html = body
        email_exp = exportador_id.email

        return self.enviar_email(
            template=template, email_exportador=email_exp
        )

