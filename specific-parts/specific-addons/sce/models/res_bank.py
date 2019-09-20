# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning


class ResBank(models.Model):
    _inherit = "res.bank"
    _name = "res.bank"
