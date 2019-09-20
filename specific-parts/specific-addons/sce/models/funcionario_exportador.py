# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning


class FuncionarioEmpresa(models.Model):

    _name = "funcionario.exportador"
    _description = "Viculo do funcionario, empresa e master da empresa"

    # _sql_constraints = [
    #     ('partner_funcionario_exportador_unique',
    #      'unique(funcionario_id, exportador_id)',
    #      'Este usuário já foi vinculado a este exportador')]

    exportador_id = fields.Many2one(
        string='Exportador',
        comodel_name='exportador',
    )

    funcionario_id = fields.Many2one(
        string='Funcionário',
        comodel_name='res.partner',
    )

    name_funcionario = fields.Char(
        string='Nome',
        related='funcionario_id.name',
    )

    cpf_cnpj_funcionario = fields.Char(
        string='CPF',
        related='funcionario_id.cpf_cnpj',
    )

    email_funcionario = fields.Char(
        string='Email',
        related='funcionario_id.email',
    )

    mobile_funcionario = fields.Char(
        string='Telefone',
        related='funcionario_id.mobile',
    )

    @api.multi
    def verifica_usuario(self, parent_id=False):
        parent_id = parent_id if parent_id else self.exportador_id.parent_id.id
        # Somente o parent_id pode add/remove funcionário
        if self.env.user.partner_id.id != parent_id:
            raise Warning(u'Somente o Contato Principal pode '
                          u'adicionar ou remover funcionários.')

    @api.multi
    def create(self, vals):
        parent_id = self.env['exportador'].browse(
            vals['exportador_id']).parent_id.id
        self.verifica_usuario(parent_id=parent_id)

        return super(FuncionarioEmpresa, self).create(vals)

    @api.multi
    def unlink(self):
        self.verifica_usuario()

        return super(FuncionarioEmpresa, self).unlink()
