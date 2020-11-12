# -*- coding:utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import api, fields, models

class CustomerCompanycusnewFields(models.Model):
    _inherit = 'res.company'

    h_phone= fields.Char("Header phone")
    vat2= fields.Char("VAT")
    svat = fields.Char("SVAT")
    br_number = fields.Char("BR Number")