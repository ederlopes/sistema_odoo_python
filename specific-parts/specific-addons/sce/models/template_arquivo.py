# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning
from tempfile import TemporaryFile
import base64
import sys, os

TIPO_ARQUIVO = [('DECLARACAO_CONFORMIDADE_MPME',
                 'DECLARAÇÃO DE CONFORMIDADE - MPME'),
                ('DECLARACAO_COMPROMISSO_MPME',
                 'DECLARAÇÃO DE COMPROMISSO - MPME'),
                ('DECLARACAO_ANTI_CORRUPCAO_MPME',
                 'DECLARAÇÃO DE ANTI-CORRUPÇÃO - MPME')]


class TemplateArquivo(models.Model):
    _name = "template.arquivo"

    name = fields.Char(
        string="Descrição do arquivo"
    )

    disclaimer = fields.Html(
        string='Disclaimer do Arquivo',
        required=True,
    )

    arquivo = fields.Binary(
        string='Documento',
    )

    nome_arquivo = fields.Char(
        string="Nome do Arquivo"
    )

    tipo_arquivo = fields.Selection(
        string=u'Tipo de Solicitante',
        selection=TIPO_ARQUIVO,
        required=True,
    )

    attachment_id = fields.Many2one(
        comodel_name='ir.attachment',
    )

    active = fields.Boolean(
        'Active',
        default=True,
        readonly=True,
    )

    @api.model
    def create(self, vals):
        self.search([('tipo_arquivo', '=', vals['tipo_arquivo'])]).write({
            'active': False})

        ext = vals['nome_arquivo'].split('.')[-1:][0]
        nome_arquivo = '{}.{}'.format(vals['tipo_arquivo'], ext)
        vals['nome_arquivo'] = nome_arquivo

        att_id = self.env['ir.attachment'].sudo().create({
            'name': nome_arquivo,
            'datas': vals['arquivo'],
        })

        res = super(TemplateArquivo, self).create(vals)

        res.attachment_id = att_id.id

        return res
