# -*- coding: utf-8 -*-
from odoo.tests.common import SingleTransactionCase, at_install, post_install
from odoo import fields


@post_install(True)
class TestCadastroExportador(SingleTransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestCadastroExportador, cls).setUpClass()

        cls.today = fields.Date.today()

        # Cria Usuário
        cls.user_id = cls.env['res.users'].create(
            {'login': 'teste@abgf.gov.br',
             'cpf_cnpj': '004.025.200-09',
             'name': 'Usuário Teste',
             'password': 'password', })

        # Cria Exportador (Empresa)
        cls.exportador_id = cls.env['res.partner'].create({
            'name': 'Empresa Teste',
            'razao_social': 'Empresa Teste',
            'email': 'email@empresa.com',
            'cpf_cnpj': '59.188.420/0001-96',
            'street': 'Rua do Exportador',
            'street2': 'Nº 10',
            'country_id': 31,
            'state_id': 30,
            'city': 'Rio de Janeiro',
            'zip': '20251-987',
            'parent_id': cls.user_id.partner_id.id,
            'is_company': True,
        })

        # Socio do Exportador
        cls.socio_ids = cls.env['socio'].create({
            'name': 'Socio 1',
            'tipo_socio': 'PF',
            'cpf_cnpj': '907.700.650-82',
            'percentual': 100.00,
            'partner_id': cls.exportador_id.id,
        })

        # Pega objeto modalidade PÓS
        modalidade = cls.env['modalidade'].search([('sigla', '=', 'PÓS')])
        cls.exportador_linha_negocio_ids = \
            cls.env['exportador.linha.negocio'].create({
                'partner_id': cls.exportador_id.id,
                'linha_negocio_id': 1,
                'modalidade_id': modalidade.id,
            })

    def test_status_inicial_exportador(self):
        '''
        Verifica se a empresa criada entrou desativada
        :return:
        '''
        self.assertFalse(self.exportador_id.active)

    def test_aprova_exportador(self):
        '''
        Aprova o exportador através do método no wizard, salvando o parecer
        técnico.
        :return:
        '''
        self.env.context['active_ids'] = [self.exportador_id.id]
        parecer_tecnico_id = \
            self.env['parecer.tecnico.exportador.wizard'].create({
                'parecer_tecnico': 'Parecer Técnico aprovado',
                'data_recomendacao': self.today, })
        parecer_tecnico_id.aprovar()

        self.assertTrue(self.exportador_id.data_recomendacao)
        self.assertEqual(self.exportador_id.parecer_tecnico,
                         '<p>Parecer Técnico aprovado</p>')
        self.assertTrue(self.exportador_id.active)

    def test_reprova_exportador(self):
        '''
        Reprova o exportador através do método no wizard, salvando o parecer
        técnico reprovado.
        :return:
        '''
        # Aprova Exportador
        self.env.context['active_ids'] = [self.exportador_id.id]
        parecer_tecnico_id = \
            self.env['parecer.tecnico.exportador.wizard'].create({
                'parecer_tecnico': 'Parecer Técnico reprovado',
                'data_recomendacao': self.today, })
        parecer_tecnico_id.reprovar()

        self.assertTrue(self.exportador_id.data_recomendacao, self.today)
        self.assertEqual(self.exportador_id.parecer_tecnico,
                         '<p>Parecer Técnico reprovado</p>')
        self.assertFalse(self.exportador_id.active)
