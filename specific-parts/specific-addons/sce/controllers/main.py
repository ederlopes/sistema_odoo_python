# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import werkzeug

from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request, route

_logger = logging.getLogger(__name__)


class AuthSignupHome(AuthSignupHome):

    @route('/web/confirmar', auth='public')
    def rota_confirmar(self, **kw):
        '''
        Rota para confirmação do email e ativação do usuário criado.

        :param kw: auth_login = token de confirmação
        :return: rota login
        '''
        token = kw.get('auth_login') or False

        res = request.env['res.users'].sudo().search([
            ('token', '=', token),
            ('active', '=', False)])

        if len(res) == 1 and token is not False:
            res.active = True
            request.params['auth_login'] = ''
            url = '/web/login?' + werkzeug.url_encode(
                {
                    'message': 'Conta ativada com sucesso!',
                    'login': res.email
                })
        else:
            url = '/web/login?' + werkzeug.url_encode(
                {
                    'error': 'Usuário não encontrado ou já ativado!',
                    'login': ''
                })

        return http.redirect_with_hash(url)

    @route()
    def web_auth_signup(self, *args, **kw):
        # Setar variavel para identificar processo
        request.params.update(verificar_email='True')

        return super(AuthSignupHome, self).web_auth_signup(*args, **kw)

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key)
                  for key in ('login', 'name', 'password', 'cpf_cnpj')}

        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values,
                                                                     token)
        request.env.cr.commit()

    @http.route()
    def web_login(self, redirect=None, **kw):
        if request.params.get('verificar_email'):
            request.params['login_success'] = False
            company = request.env['res.company'].sudo().search([])
            values = {'dados': request.params, 'company': company}

            return request.render("sce.verificar_email", values)

        return super(AuthSignupHome, self).web_login(redirect=redirect, **kw)
