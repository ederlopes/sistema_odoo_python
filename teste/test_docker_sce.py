# -*- coding: utf-8 -*-
import os
from time import sleep
import imp
teste = imp.load_source('TestSce', '/odoo/teste/test_sce.py')

path = os.getcwd().replace('/teste', '')

USUARIOS = {
    'admin': {'usuario': 'admin',
              'senha': 'admin', },
    'exportador': {'usuario': 'sce_test@mailinator.com',
                   'senha': 'teste',
                   'name': 'Usuário Teste',
                   'cpf': '253.270.340-70', },
    'exportador2': {'usuario': 'sce_test2@mailinator.com',
                    'senha': 'teste2',
                    'name': 'Usuário Teste2',
                    'cpf': '546.202.320-09', }, }
USUARIOS_FUNC = {
    'Analista': {'usuario': 'analista_sce@mailinator.com',
                 'senha': 'teste',
                 'name': 'Analista ABGF Teste',
                 'cpf': '560.562.610-85'},
    'Gerente': {'usuario': 'gerente_sce@mailinator.com',
                'senha': 'teste',
                'name': 'Gerente ABGF Teste',
                'cpf': '868.888.710-10'}, }
EMPRESAS = {
    'empresa': {
        'name': 'Empresa 1',
        'razao_social': 'Razão Social Empresa 1',
        'email': 'empresa1@empresa.com',
        'cpf_cnpj': '61.259.927/0001-35',
        'street': 'Rua Empresa 1',
        'street2': 'n 10',
        'state': 'Rio de Janeiro (BR)',
        'city': 'Rio de Janeiro',
        'zip': '20251-061',
    },
    'empresa2': {
        'name': 'Empresa 2',
        'razao_social': 'Razão Social Empresa 2',
        'email': 'empresa2@empresa.com',
        'cpf_cnpj': '23.187.602/0001-03',
        'street': 'Rua Empresa 2',
        'street2': 'n 20',
        'state': 'Rio de Janeiro (BR)',
        'city': 'Rio de Janeiro',
        'zip': '20251-061',
    }
}


def sessao(func):
    def criar_session(self):
        '''
        Cria sessão para executar ações direto sem a interface
        :return: sessão criada
        '''
        print('[TESTE] ------------ CRIANDO SESSÃO')
        self.session.open(db=self.banco)
        sleep(2)
        res = func(self)
        sleep(2)
        self.session.close()

        return res

    return criar_session


class TestDockerSce(teste.TestSce):
    def start_odoo(self, banco=False):
        '''

        :return:
        '''

        print('[TESTE] ------------ START ODOO')
        print('[TESTE] ------------ MATANDO PROCESSO')
        os.system("killall start_odoo &")
        os.system("killall start_odoo &")

        if banco:
            print('[TESTE] ------------ INICIANDO COM BANCO')
            os.system("bin/start_odoo -d {} &".format(self.banco))
        else:
            print('[TESTE] ------------ INICIA SEM BANCO')
            os.system("bin/start_odoo &")
        sleep(5)

def main():
    teste = TestDockerSce()
    teste.cadastra_empresa(empresa='empresa')


if __name__ == '__main__':
    main()
