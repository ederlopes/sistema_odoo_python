# -*- coding: utf-8 -*-
import os
import sys
from time import sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

path = os.path.dirname(os.path.dirname(__file__))

sys.path[0:0] = [
  '{}/src/py3o.template'.format(path),
  '{}/src/py3o.formats'.format(path),
  '{}/src/anybox.recipe.odoo'.format(path),
  '{}/parts/odoo'.format(path),
  '{}/eggs/num2words-0.5.10-py3.5.egg'.format(path),
  '{}/eggs/ipython-5.8.0-py3.5.egg'.format(path),
  '{}/eggs/ipdb-0.12-py3.5.egg'.format(path),
  '{}/eggs/signxml-2.6.0-py3.5.egg'.format(path),
  '{}/eggs/sh-1.12.14-py3.5.egg'.format(path),
  '{}/eggs/email_validator-1.0.4-py3.5.egg'.format(path),
  '{}/eggs/html2text-2018.1.9-py3.5.egg'.format(path),
  '{}/eggs/numpy-1.16.4-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/satcomum-1.1-py3.5.egg'.format(path),
  '{}/eggs/ofxparse-0.20-py3.5.egg'.format(path),
  '{}/eggs/graypy-1.1.2-py3.5.egg'.format(path),
  '{}/eggs/pandas-0.24.2-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/decorator-4.4.0-py3.5.egg'.format(path),
  '{}/eggs/docutils-0.14-py3.5.egg'.format(path),
  '{}/eggs/feedparser-5.2.1-py3.5.egg'.format(path),
  '{}/eggs/gevent-1.4.0-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/Jinja2-2.10.1-py3.5.egg'.format(path),
  '{}/eggs/lxml-4.3.3-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/libsass-0.19.1-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/Mako-1.0.12-py3.5.egg'.format(path),
  '{}/eggs/mock-3.0.5-py3.5.egg'.format(path),
  '{}/eggs/passlib-1.7.1-py3.5.egg'.format(path),
  '{}/eggs/Pillow-6.0.0-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/psutil-5.6.2-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/psycopg2-2.8.2-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/pydot-1.4.1-py3.5.egg'.format(path),
  '{}/eggs/pyldap-3.0.0.post1-py3.5.egg'.format(path),
  '{}/eggs/pyparsing-2.4.0-py3.5.egg'.format(path),
  '{}/eggs/PyPDF2-1.26.0-py3.5.egg'.format(path),
  '{}/eggs/pyserial-3.4-py3.5.egg'.format(path),
  '{}/eggs/python_dateutil-2.8.0-py3.5.egg'.format(path),
  '{}/eggs/pyusb-1.0.0b2-py3.5.egg'.format(path),
  '{}/eggs/qrcode-6.1-py3.5.egg'.format(path),
  '{}/eggs/reportlab-3.5.23-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/requests-2.22.0-py3.5.egg'.format(path),
  '{}/eggs/suds_jurko-0.6-py3.5.egg'.format(path),
  '{}/eggs/vatnumber-1.2-py3.5.egg'.format(path),
  '{}/eggs/vobject-0.9.6.1-py3.5.egg'.format(path),
  '{}/eggs/Werkzeug-0.15.4-py3.5.egg'.format(path),
  '{}/eggs/XlsxWriter-1.1.8-py3.5.egg'.format(path),
  '{}/eggs/xlwt-1.3.0-py3.5.egg'.format(path),
  '{}/eggs/anybox.testing.datetime-0.5-py3.5.egg'.format(path),
  '{}/eggs/unittest2-1.1.0-py3.5.egg'.format(path),
  '{}/eggs/traceback2-1.4.0-py3.5.egg'.format(path),
  '{}/eggs/six-1.12.0-py3.5.egg'.format(path),
  '{}/eggs/argparse-1.4.0-py3.5.egg'.format(path),
  '{}/eggs/python_stdnum-1.11-py3.5.egg'.format(path),
  '{}/eggs/urllib3-1.25.3-py3.5.egg'.format(path),
  '{}/eggs/idna-2.8-py3.5.egg'.format(path),
  '{}/eggs/certifi-2019.3.9-py3.5.egg'.format(path),
  '{}/eggs/python_ldap-3.2.0-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/beautifulsoup4-4.7.1-py3.5.egg'.format(path),
  '{}/eggs/MarkupSafe-1.1.1-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/greenlet-0.4.15-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/zc.recipe.egg-2.0.7-py3.5.egg'.format(path),
  '{}/eggs/dnspython-1.16.0-py3.5.egg'.format(path),
  '{}/eggs/pyjon.utils-0.7-py3.5.egg'.format(path),
  '{}/eggs/Genshi-0.7.3-py3.5.egg'.format(path),
  '{}/eggs/pyOpenSSL-18.0.0-py3.5.egg'.format(path),
  '{}/eggs/eight-0.4.2-py3.5.egg'.format(path),
  '{}/eggs/defusedxml-0.6.0-py3.5.egg'.format(path),
  '{}/eggs/cryptography-2.2.2-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/asn1crypto-0.24.0-py3.5.egg'.format(path),
  '{}/eggs/traitlets-4.3.2-py3.5.egg'.format(path),
  '{}/eggs/simplegeneric-0.8.1-py3.5.egg'.format(path),
  '{}/eggs/Pygments-2.4.2-py3.5.egg'.format(path),
  '{}/eggs/prompt_toolkit-1.0.16-py3.5.egg'.format(path),
  '{}/eggs/pickleshare-0.7.5-py3.5.egg'.format(path),
  '{}/eggs/pexpect-4.7.0-py3.5.egg'.format(path),
  '{}/eggs/docopt-0.6.2-py3.5.egg'.format(path),
  '{}/eggs/linecache2-1.0.0-py3.5.egg'.format(path),
  '{}/eggs/pyasn1_modules-0.2.5-py3.5.egg'.format(path),
  '{}/eggs/pyasn1-0.4.5-py3.5.egg'.format(path),''
  '{}/eggs/soupsieve-1.9.1-py3.5.egg'.format(path),
  '{}/eggs/future-0.16.0-py3.5.egg'.format(path),
  '{}/eggs/cffi-1.12.3-py3.5-linux-x86_64.egg'.format(path),
  '{}/eggs/ipython_genutils-0.2.0-py3.5.egg'.format(path),
  '{}/eggs/wcwidth-0.1.7-py3.5.egg'.format(path),
  '{}/eggs/ptyprocess-0.6.0-py3.5.egg'.format(path),
  '{}/eggs/pycparser-2.19-py3.5.egg'.format(path),
  '{}/lib/python3.5/site-packages'.format(path),
  ]

from anybox.recipe.odoo.runtime.session import Session

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


def sessao(func, start_odoo=False):
    def criar_session(self):
        '''
        Cria sessão para executar ações direto sem a interface
        :return: sessão criada
        '''
        print('[TESTE] ------------ CRIANDO SESSÃO')

        res = os.popen('ps aux | grep start_odoo').read()
        if 'start_odoo' in res and 'grep' not in res:
            if '-i' in res:
                while True:
                    if '-i' not in os.popen('ps aux | grep start_odoo').read():
                        break

            os.system("killall start_odoo")
            os.system("killall start_odoo")

        if not self.session:
            pasta_proj = os.getcwd().replace(
                '/specific-parts/specific-addons/sce', '')
            self.session = Session('{}/etc/odoo.cfg'.format(pasta_proj),
                                   pasta_proj)
        try:
            self.session.open(db=self.banco)
            sleep(2)
            res = func(self)
            sleep(2)
            self.session.close()
        except:
            if start_odoo:
                self.start_odoo()

        return res
    return criar_session


class TestSce(object):
    def __init__(self, banco='sce', background=True):
        if background:
            display = Display(visible=0, size=(800, 600))
            display.start()

        self.banco = banco

        binary = FirefoxBinary('/usr/bin/firefox')
        self.driver = webdriver.Firefox(firefox_binary=binary)
        p = webdriver.FirefoxProfile()
        self.session = False

        self.cria_funcionarios()
        self.criar_banco()
        self.criar_usuarios()

    def start_odoo(self, banco=False):
        '''
        Inicia o ODOO para que o driver do selenium faça as automações
        :param teste: inicia os testes automatizados do ODOO e mata o processo
        logo apoós
        :return:
        '''

        print('[TESTE] ------------ START ODOO')
        print('[TESTE] ------------ MATANDO PROCESSO')
        os.system("killall start_odoo &")
        os.system("killall start_odoo &")

        if banco:
            print('[TESTE] ------------ INICIANDO COM BANCO')
            os.system("start_odoo -d {} &".format(self.banco))
        else:
            print('[TESTE] ------------ INICIA SEM BANCO')
            os.system("start_odoo &")
        sleep(5)

    def criar_banco(self):
        os.system("killall start_odoo &")
        os.system("killall start_odoo &")
        self.start_odoo()
        sleep(5)
        self.driver.get('http://localhost:8069/web/database/manager')
        try:
            banco = self.wait_element(element=self.banco,
                                      by=By.PARTIAL_LINK_TEXT,
                                      click=False)
            if banco:
                self.wait_element(
                    element="//*/div[a[text()[contains(.,'{}')]]]"
                            "/div/button[text()[contains(.,'Delete')]]"
                            "".format(self.banco),
                    by=By.XPATH)
                self.wait_element(element="//*/div[@class='modal-content']/"
                                          "form/div[@class='modal-footer']/"
                                          "input[@value='Delete']",
                                  by=By.XPATH)
        except:
            pass

        self.wait_element("//*/button[text()='Create Database']", by=By.XPATH)
        self.wait_element("name", by=By.NAME, val=self.banco, click=False)
        self.wait_element("login", by=By.NAME, val='admin', click=False)
        self.wait_element("password", by=By.NAME, val='admin', click=False)
        self.wait_element("//*/select[@name='lang']/option[@value='pt_BR']",
                          by=By.XPATH)
        self.wait_element("//*/select[@name='country_code']"
                          "/option[@value='br']",
                          by=By.XPATH)
        self.wait_element("//*/input[@type='submit']", by=By.XPATH)

        self.busca(busca='SCE')

        self.wait_element(element="//*/button[text()='Instalar']", by=By.XPATH,
                          tempo=60)

        self.body_hotkey(key='b')

        self.logout(tempo=60)

    def logout(self, tempo=20):
        try:
            self.wait_element(element="//*/ul[@class='o_menu_systray']/li/a",
                              by=By.XPATH, tempo=tempo)
            self.wait_element(element="Sair", by=By.PARTIAL_LINK_TEXT)
        except TimeoutException:
            self.wait_element(element='Administrator', by=By.PARTIAL_LINK_TEXT)
            self.wait_element(element='Sair', by=By.PARTIAL_LINK_TEXT)

    def criar_usuarios(self):
        '''
        Cria usuário funcionário ABGF e dois exportadores

        :return:
        '''
        self.criar_usuario_exportador(usuario='exportador2')
        self.criar_usuario_exportador(usuario='exportador')

    def wait_element(self, element, by, val=False, click=True, tempo=20):
        wait = WebDriverWait(self.driver, tempo)
        e = wait.until(EC.visibility_of_element_located((by, element)))
        if val:
            e.clear()
            e.send_keys(Keys.HOME + val)

        if click:
            e.click()

        return e

    def login(self, usuario):
        '''
        Faz login no ODOO
        :param usuario:
        :return:
        '''
        self.driver.get('http://localhost:8069/web/login')
        self.preenche_login_senha(usuario=usuario)
        self.wait_element(element="//button[@type='submit']",
                          by=By.XPATH)

    def preenche_login_senha(self, usuario):
        '''
        Preenche campos de login e senha
        :param usuario: Usuário que irá se logar
        :return:
        '''
        self.wait_element(element='login', by=By.ID,
                          val=USUARIOS[usuario]['usuario'], click=False)
        self.wait_element(element='password', by=By.ID,
                          val=USUARIOS[usuario]['senha'], click=False)

    def criar_usuario_exportador(self, usuario):
        '''
        Cria usuário exportador conforme usuário informado
        :param usuario: usuário a ser criado
        :return:
        '''
        self.driver.get('http://localhost:8069/web/login')

        self.wait_element(element='Não possui uma conta?',
                          by=By.PARTIAL_LINK_TEXT)
        self.preenche_login_senha(usuario=usuario)
        self.wait_element(element='name', by=By.ID,
                          val=USUARIOS[usuario]['name'], click=False)
        self.wait_element(element='cpf_cnpj', by=By.ID,
                          val=USUARIOS[usuario]['cpf'])

        element = self.wait_element(element='confirm_password', by=By.ID,
                                    val=USUARIOS[usuario]['senha'],
                                    click=False)
        element.send_keys(Keys.DOWN)
        element.send_keys(Keys.RETURN)
        self.confirma_email_validacao(usuario=usuario)

    def primeira_linha_tree_view(self):
        return self.wait_element(element='o_data_cell', by=By.CLASS_NAME,
                                 click=False)

    def voltar_pagina(self):
        sleep(1)
        self.driver.back()

    def body_hotkey(self, key):
        sleep(1)
        body = self.wait_element(element='body', by=By.TAG_NAME, click=False)
        body.send_keys(Keys.ALT + key)

    def confirma_email_validacao(self, usuario):
        '''
        Acessa o mailinator para confirmar o e-mail
        :param usuario:
        :return:
        '''
        self.driver.get('https://www.mailinator.com/')
        element = self.wait_element(element='form-control', by=By.CLASS_NAME,
                                    val=USUARIOS[usuario]['usuario'],
                                    click=False)
        element.send_keys(Keys.RETURN)
        self.wait_element(element="//*/td[@class='ng-binding']"
                                  "[contains(text(),'moments ago')]",
                          by=By.XPATH)
        self.wait_element(element="Bem-vindo a ABGF!", by=By.PARTIAL_LINK_TEXT)
        self.driver.switch_to.frame('msg_body')
        self.wait_element('Go to My', by=By.PARTIAL_LINK_TEXT)
        self.driver.switch_to.default_content()
        self.driver.switch_to_window(self.driver.window_handles[0])
        self.fecha_aba()

    def fecha_aba(self):
        '''
        Fecha abas a mais, se existir. Torna a primeira aba como principal
        :return:
        '''
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])

    def acessa_menu(self, usuario=False):
        '''
        Acessa o menu principal do ODOO 12
        :param usuario: Se informado usuário, o sistema loga com ele
        :return:
        '''
        if usuario:
            self.login(usuario=usuario)
        try:
            self.wait_element(element='//*[@class="full"]',
                              by=By.XPATH)
        except:
            self.confirma_email_validacao(usuario=usuario)
            self.acessa_menu(usuario=usuario)

    def acessa_menu_sce(self, usuario=False):
        '''
        Acessa o menu do SCE, submenu do menu principal
        :param usuario: Se informado usuário, o sistema loga com ele
        :return:
        '''
        self.acessa_menu(usuario=usuario)
        self.wait_element(element='SCE', by=By.PARTIAL_LINK_TEXT)

    def acessa_menu_config(self, usuario=False):
        '''
        Acessa o menu de configurações
        :param usuario: Se informado usuário, o sistema loga com ele
        :return:
        '''
        self.acessa_menu(usuario=usuario)
        settings = self.wait_element(element='Settings',
                                     by=By.PARTIAL_LINK_TEXT, click=False)
        if settings:
            settings.click()
        else:
            self.wait_element(element='Configurações',
                              by=By.PARTIAL_LINK_TEXT)

    def acessar_menu_cadastro(self, usuario=False):
        self.acessa_menu_sce(usuario=usuario)
        self.wait_element(element='Cadastro', by=By.PARTIAL_LINK_TEXT)

    def acessar_sub_menu_cadastro_empresa(self, usuario=False):
        self.acessar_menu_cadastro(usuario=usuario)
        self.wait_element("Empresa", by=By.PARTIAL_LINK_TEXT)

    def busca(self, busca, click_linha=False):
        '''
        Acessa o menu de busca padrão em todas as telas do ODOO
        :param busca: busca a ser feita
        :return:
        '''
        input_search = self.wait_element(
            element="//input[@class='o_searchview_input']", by=By.XPATH,
            val=busca, click=False, tempo=60)
        input_search.send_keys(Keys.RETURN)
        if click_linha:
            self.primeira_linha_tree_view().click()

    def cadastra_empresa(self, empresa):
        '''
        Cadastro de empresa
        :param empresa: dados da empresa a ser cadastrada
        :return:
        '''
        print('[TESTE] ------------ INICIA CADASTRO DE EMPRESA')
        self.acessar_sub_menu_cadastro_empresa(usuario='exportador')

        self.acessar_sub_menu_cadastro_empresa()
        self.body_hotkey('c')

        print('[TESTE] ------------ PREENCHE DADOS')
        for campo in EMPRESAS[empresa].keys():
            if campo == 'state':
                elem = self.wait_element(
                    element="//*[@class='o_input_dropdown']/input",
                    by=By.XPATH, click=False)
                elem.send_keys(EMPRESAS[empresa].get(campo))
                Keys.DOWN
                Keys.RETURN
            else:
                self.wait_element(element=campo, by=By.NAME,
                                  val=EMPRESAS[empresa].get(campo),
                                  click=False)

        self.body_hotkey('s')
        print('[TESTE] ------------ INCLUI SÓCIO')
        self.inclui_socio()
        print('[TESTE] ------------ CADASTRA LINHA DE NEGÓCIO')
        self.inclui_linha_negocio()
        sleep(2)
        print('[TESTE] ------------ ENVIAR CADASTRO')
        self.wait_element(element='enviar_cadastro', by=By.NAME)

    def inclui_linha_negocio(self):
        self.acessar_sub_menu_cadastro_empresa()
        # Busca Empresa
        self.busca(busca='Empresa 1', click_linha=True)

        self.body_hotkey(key='a')

        self.wait_element(element='Linhas de Negócios',
                          by=By.PARTIAL_LINK_TEXT)

        self.wait_element(element='Adicionar uma linha',
                          by=By.PARTIAL_LINK_TEXT)

        e = self.wait_element(
           element="//*/div[@name='linha_negocio_id']/*/input",
           by=By.XPATH)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.RETURN)

        e = self.wait_element(element="//*/div[@name='modalidade_id']/*/input",
                              by=By.XPATH)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.RETURN)
        sleep(1)

        e = self.wait_element(
            element="//*/div[@name='tipo_financiamento_id']/*/input",
            by=By.XPATH)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.RETURN)
        sleep(1)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.RETURN)
        sleep(1)

        # Aperta ALT + s para salvar empresa
        self.body_hotkey('s')

    def inclui_socio(self):
        self.acessar_sub_menu_cadastro_empresa()
        # Busca Empresa
        self.busca(busca='Empresa 1', click_linha=True)

        self.body_hotkey(key='a')
        self.wait_element(element='Sócios', by=By.PARTIAL_LINK_TEXT)

        self.wait_element(element='Adicionar uma linha',
                          by=By.PARTIAL_LINK_TEXT)

        # Preenche os dados do sócio
        self.wait_element(
            element='//*[@class="modal-content"]//*/input[@name="name"]',
            by=By.XPATH, val='Sócio Teste 1')

        tipo_socio = self.wait_element(element='tipo_socio', by=By.NAME)
        tipo_socio.send_keys(Keys.DOWN)

        self.wait_element(
            element='//*[@class="modal-content"]//*/input[@name="cpf_cnpj"]'
            '[@class="o_field_widget o_input o_required_modifier"]',
            by=By.XPATH, val='614.034.900-15')

        self.wait_element(element='percentual', by=By.NAME, val='100,00')

        # Aperta ALT + o para criar sócio
        self.body_hotkey('o')

        # Aperta ALT + s para salvar empresa
        self.body_hotkey('s')

    @sessao
    def cria_funcionarios(self):
        '''
        Cria usuário e adiciona ao grupo de funcionário ABGF

        * Utiliza a sessão, não usa o selenium
        :return:
        '''
        groups = self.session.env['res.groups']
        for func in USUARIOS_FUNC:
            group_id = groups.search([('name', '=', func)])

            count_user = self.session.env['res.users'].search_count(
                [('login', '=', USUARIOS_FUNC[func]['usuario'])])
            partner = self.session.env['res.partner'].search(
                [('email', '=', USUARIOS_FUNC[func]['usuario'])])
            if count_user == 0:
                res = self.session.env['res.users'].create(
                    {'name': USUARIOS_FUNC[func]['name'],
                     'password': USUARIOS_FUNC[func]['senha'],
                     'login': USUARIOS_FUNC[func]['usuario'],
                     'email': USUARIOS_FUNC[func]['usuario'],
                     'cpf_cnpj': USUARIOS_FUNC[func]['cpf'],
                     'partner_id': partner.id if partner else False})

                res.groups_id = False
                res.groups_id = group_id

        self.session.cr.commit()

    @sessao
    def deleta_empresa(self):
        '''
        Deleta todas as empresas criadas para o teste
        :return:
        '''
        try:
            exportador_ids = self.session.env['exportador'].sudo().search(
                ['|', ('active', '=', True), ('active', '=', False)])
            if exportador_ids:
                for exportador_id in exportador_ids:
                    for ln in exportador_id.exportador_linha_negocio_ids:
                        ln.sudo().unlink()

                    exportador_id.sudo().unlink()
                    self.session.cr.commit()
        except:
            pass

    @sessao
    def deleta_usuario(self):
        '''
        Deleta todos os usuários criados para o teste
        :return:
        '''
        for user in USUARIOS:
            if user != 'admin':
                print('[TESTE] ------------ DELETA USUÁRIO: {}'.format(
                    USUARIOS[user]['usuario']))
                user_id = self.session.env['res.users'].sudo().search(
                    [('login', '=', USUARIOS[user]['usuario'])])
                partner_id = self.session.env['res.partner'].sudo().search(
                    [('email', '=', USUARIOS[user]['usuario'])])
                print('[TESTE] ------------ usuario: {}; partner: {}.'.format(
                    user_id.name, partner_id.name))
                if len(user_id):
                    user_id.sudo().unlink()
                if len(partner_id):
                    if partner_id.user_id:
                        partner_id.user_id.sudo().unlink()
                    partner_id.sudo().unlink()

                self.session.cr.commit()


def main():
    teste = TestSce(banco='sce1', background=False)
    teste.cadastra_empresa(empresa='empresa')


if __name__ == '__main__':
    main()
