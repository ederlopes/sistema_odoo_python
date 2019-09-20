# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pandas as pd
import sys, os, csv, io
from time import gmtime, strftime
from datetime import datetime
import requests


class CotacaoDiaria(models.Model):
    _name = 'cotacao.diaria'
    _description = 'Cotação Diária'
    _rec_name = 'currency_id'

    data_cadastro = fields.Date(
        string=u'Data de Cadastro',
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
    )

    taxa_cotacao_compra = fields.Float(
        string='Taxa de cotação de compra',
        digits=(12, 5),
    )

    taxa_cotacao_venda = fields.Float(
        string='Taxa de cotação venda',
        digits=(12, 5),
    )

    paridade_compra = fields.Float(
        string='Paridade de compra',
        digits=(12, 5),
    )

    paridade_venda = fields.Float(
        string='Paridade venda',
        digits=(12, 5),
    )

    id_user = fields.Many2one(
        'res.users',
        'Usuario',
        default=lambda self: self.env.user
    )


    @api.multi
    def cotacao_diaria(self):
        contador = 0
        data = datetime.now()
        hj = data.today()

        if hj.weekday() < 5:
            df = self.ler_arquivo_cvs()

            dados_moeda = self.monta_dicionario_moeda()

            for index, col in df.iterrows():
                if col['SIGLA_MOEDA'] in dados_moeda:
                    vals = {
                        'data_cadastro': col['DATA'],
                        'taxa_cotacao_compra': col['TAXA_COMPRA'].replace(",", "."),
                        'taxa_cotacao_venda': col['TAXA_VENDA'].replace(",", "."),
                        'paridade_compra': col['PARIDADE_COMPRA'].replace(",", "."),
                        'paridade_venda': col['PARIDADE_VENDA'].replace(",", "."),
                        'currency_id': dados_moeda[col['SIGLA_MOEDA']],
                    }
                    contador += 1
                    self.create(vals)
            if (contador > 0):
                self.notifica_nova_operacao(contador)

        return True


    def ler_arquivo_cvs(self):
        data = datetime.now()
        ano = data.year
        mes = '{:02d}'.format(data.month)
        dia = '{:02d}'.format(data.day - 1)
        url = 'http://www4.bcb.gov.br/download/fechamento/{}{}{' \
              '}.csv'.format(ano, mes, dia)
        df = pd.read_csv(url, sep=';', quotechar='"', encoding='utf8',
                         names=['DATA', 'CODIGO_MOEDA', 'TIPO_COTACAO',
                                'SIGLA_MOEDA', 'TAXA_COMPRA', 'TAXA_VENDA',
                                'PARIDADE_COMPRA', 'PARIDADE_VENDA'])
        df.iterrows()
        return df

    def monta_dicionario_moeda(self):
        array_campos = {}

        # PEGANDO TODA A TAVELA DE MOEDAS PARA FAZER VINCULO COM A COTACAO
        domain = [('active', '=', 1)]
        dados_moedas_ativa = self.env['res.currency'].search(domain)

        domain = [('active', '=', 0)]
        dados_moedas_desativada = self.env['res.currency'].search(domain)

        for moedas_ativa in dados_moedas_ativa:
            array_campos[moedas_ativa.name] = moedas_ativa.id

        for moedas_desetivada in dados_moedas_desativada:
            array_campos[moedas_desetivada.name] = moedas_desetivada.id

        return array_campos

    def notifica_nova_operacao(self, param_contador):
        template = self.env.ref('cotacao_moeda.email_notificacao_cotacao')

        body = template.body_html
        registros_processados = '{}'.format(param_contador)
        body = body.replace('--registros_processados--', '{}'.format(
            registros_processados))
        url_padrao = self.env['ir.config_parameter'].sudo()\
            .get_param('web.base.url')
        url = '{}/web#id={}&model=cotacao_diaria&view_type=form'.format(
            url_padrao, self.id)
        url_img = '{}/sce/static/src/img/sce_logo.png'.format(url_padrao)
        body = body.replace('--url--', url)
        body = body.replace('--url_img--', url_img)
        template.body_html = body

        return self.enviar_email(template=template)

    def prepara_email(self, template):
        if template:

            emails = 'eder.lopes@abgf.gov.br'

            mail_values = {'subject': template.subject,
                           'body_html': template.body_html,
                           'email_from': template.email_from,
                           'email_to': emails
                           }

            return mail_values

    def enviar_email(self, template):
        mail_values = self.prepara_email(template=template)

        return self.env['mail.mail'].create(mail_values).send()