from . import models
from . import wizard
from . import controllers

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, pool):
    """
    Desabilitar regra
    """
    env = Environment(cr, SUPERUSER_ID, {})
    rule = env.ref('base.res_partner_rule_private_employee')
    if rule:
        rule.write({'active': False, })

    env['res.company'].browse(1).name = 'ABGF'

    # mail = env.ref('auth_signup.mail_template_user_signup_account_created')
    # mail_template_user_signup_account_created_verify
