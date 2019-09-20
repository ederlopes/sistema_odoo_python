# -*- coding: utf-8 -*-

from odoo import models, fields, api

TIPO_QUADRO = [('1', 'QUADROS ESTATISTICOS-378'),
               ('2', 'QUADROS ESTATISTICOS-419'),
               ('3', 'REGISTRO OPERACIONAL')]

class Quadro(models.Model):

    _name = 'susep.quadro'
    _description = 'Quadro Susep'
    _rec_name = 'nome_quadro'

    nome_quadro = fields.Char(
        string='Nome do Quadro'
    )

    tab_excel = fields.Char(
        string='Nome da TAB do Excel'
    )

    planilha_ids = fields.One2many(
        comodel_name='susep.planilha',
        inverse_name='quadro_id',
        string='Planilhas'
    )

    nome_arquivo_exportacao = fields.Char(
        string='Nome do arquivo para exportação'
    )

    numero_linhas = fields.Char(
        string='Número de linhas do arquivo'
    )

    susep_id = fields.One2many(
        comodel_name='susep.arquivos',
        inverse_name='quadro_id',
        string='Arquivo Susep',
        help='Selecione um ou mais',
    )

    tipo_quadro = fields.Selection(
        string=u'Tipo',
        selection=TIPO_QUADRO,
    )
