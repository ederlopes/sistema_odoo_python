# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pycpfcnpj import cpfcnpj
from odoo.exceptions import Warning

TIPO_SOCIO = [('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')]


class Socio(models.Model):
    _name = "socio"
    _description = "Sócios da empresa"

    name = fields.Char(
        string='Nome do Sócio',
        required=True,
    )

    cpf_cnpj = fields.Char(
        string='CPF/CNPJ',
        required=True,
    )

    percentual = fields.Float(
        string='% de participação',
        required=True,
    )

    tipo_socio = fields.Selection(
        string=u'Tipo de Sócio',
        selection=TIPO_SOCIO,
        required=True,
    )

    exportador_id = fields.Many2one(
        comodel_name='exportador',
        string='Exportador'
    )

    @api.model
    def create(self, vals):
        if cpfcnpj.validate(vals['cpf_cnpj']):
            return super(Socio, self).create(vals)

        raise Warning(u'CPF/CNPJ invalido.')
