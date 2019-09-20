# -*- coding: utf-8 -*-

from odoo import models, fields, api
import werkzeug
from passlib.context import CryptContext
from pycpfcnpj import cpfcnpj
from odoo.exceptions import Warning


class ResUsers(models.Model):
    _inherit = "res.users"

    token = fields.Char(
        string='token',
    )

    @api.model
    def create(self, vals):
        # Valida CPF
        if not cpfcnpj.validate(vals['cpf_cnpj']):
            raise Warning(u'CPF invalido.')

        pelo_exportador = False
        # Verifica se o usuário foi criado pelo exportador Master
        if not self.env.context.get('no_reset_password'):
            # Adiciona ao contexto que o e-mail enviado será o de criação
            # de usuário
            context = dict(self.env.context)
            context['no_reset_password'] = True
            context['create_user'] = False
            self.env.context = context
            pelo_exportador = True

        # Cria o usuário
        res = super(ResUsers, self).create(vals)

        # Adiciona dados ao partner
        res.partner_id.cpf_cnpj = vals['cpf_cnpj']
        res.partner_id.user_id = res.id

        # Gera token
        token = CryptContext(['pbkdf2_sha512']).encrypt(vals['password'])
        res.token = token

        # Se o cadastro foi através do exportador
        if pelo_exportador:
            res.mapped('partner_id').signup_prepare(signup_type="reset")
            # Envia email de ativação
            template = self.env.ref(
                'sce.usuario_criar_senha_email',
                raise_if_not_found=False)
            if res and template:
                template.sudo().with_context(
                    lang=res.lang,
                    auth_login=werkzeug.url_encode(
                        {'auth_login': res.token}),
                ).send_mail(res.id, force_send=True)

        # Se o cadastro foi através do site
        else:
            # Envia email de ativação
            template = self.env.ref(
                'sce.mail_template_user_signup_account_created_verify',
                raise_if_not_found=False)
            if res and template:
                template.sudo().with_context(
                    lang=res.lang,
                    auth_login=werkzeug.url_encode(
                        {'auth_login': res.token}),
                ).send_mail(res.id, force_send=True)
            # Desativa usuário
            res.active = False

        # GRUPOS
        groups = self.env['res.groups']
        group_exp_id = groups.search([('name', '=', 'Exportador')])
        res.groups_id = False
        res.groups_id = group_exp_id

        return res
