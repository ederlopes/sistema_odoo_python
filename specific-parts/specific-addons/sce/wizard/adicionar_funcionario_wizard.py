# -*- coding: utf-8 -*-
from odoo import models, fields, api
from passlib.context import CryptContext


class AdicionaFuncionarioWizard(models.TransientModel):

    _name = "adicionar.funcionario.wizard"
    _description = "Adicionar Funcionário"

    name = fields.Char(
        string='Nome',
        required=True,
    )

    email = fields.Char(
        string='Email',
        required=True,
    )

    cpf = fields.Char(
        string='CPF',
        required=True,
    )

    def create_user(self, partner_id=False):
        '''
        Cria res user para criação do usuário

        :param partner_id: se passar o partner, associa ao criado
        :return:
        '''
        user = self.env['res.users'].sudo()
        dict_user = {
            'name': self.name,
            'login': self.email,
            'email': self.email,
            'password': CryptContext(['pbkdf2_sha512']).encrypt(
                self.email)[:8],
            'cpf_cnpj': self.cpf, }

        if partner_id:
            dict_user['partner_id'] = partner_id.id

        user_id = user.create(dict_user)
        user_id.active = True

        return user_id

    def vincula_partner(self, partner_id, exportador_id):
        # Vincula o partner do funcionário a empresa exportadora
        vals = {'funcionario_id': partner_id.id,
                'exportador_id': exportador_id.id, }
        self.env['funcionario.exportador'].create(vals)

    @api.multi
    def adicionar_funcionario(self):
        '''
        Adiciona Funcionário
        :return:
        '''
        user = self.env['res.users'].sudo()
        partner = self.env['res.partner'].sudo()
        active_ids = self.env.context['active_ids'][0]
        exportador_id = partner.browse(active_ids)

        # Verifica se já existe o partner
        partner_id = partner.search(
            [('email', '=', self.email), ('cpf_cnpj', '=', self.cpf),
             ('is_company', '=', False)])

        if partner_id:
            # Verifica se existe usuário para esse partner
            if not partner_id.user_ids:
                # Verifica se existe usuário com esse login
                user_id = user.search(['&', ('login', '=', self.email),
                                       '|', ('active', '=', False),
                                            ('active', '=', True)])
                if not user_id:
                    # Cria usuário
                    self.create_user(partner_id=partner_id)
                else:
                    # Vincula partner
                    user_id.parner_id = partner_id.id
        else:
            # Cria usuário
            user_id = self.create_user()
            partner_id = user_id.partner_id

        # Vincula partner a empresa exportadora
        self.vincula_partner(partner_id, exportador_id)
