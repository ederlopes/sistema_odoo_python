# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import urls
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo import fields as odoo_fields, tools, _

from odoo.http import content_disposition, Controller, request, route

from odoo.exceptions import ValidationError, AccessError, MissingError, UserError

from odoo.tools import consteq

# --------------------------------------------------
# Misc tools
# --------------------------------------------------


class CustomerPortal(CustomerPortal):

    MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "street", "city",
                                "country_id", "cpf_cnpj"]
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "cpf_cnpj",
                               "company_name"]


    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
            values = self._prepare_portal_layout_values()
            return request.render("sce.portal_my_home", values)

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in
                          self.MANDATORY_BILLING_FIELDS}
                values.update(
                    {key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if
                     key in post})
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("sce.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(
                data.get('email')):
            error["email"] = 'error'
            error_message.append(
                _('Invalid Email! Please enter a valid email address.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        unknown = [k for k in data if
                   k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message
