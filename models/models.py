# -*- coding: utf-8 -*-
from datetime import datetime
from flectra import models, fields, api

# class smart_traiding_inventory(models.Model):
#     _name = 'smart_traiding_inventory.smart_traiding_inventory'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    age = fields.Integer(string="Age",  compute="_compute_age")
    blood_group= fields.Char(string="Blood Group")

    @api.multi
    @api.depends("birthday")
    def _compute_age(self):
      for record in self:
        today = datetime.now().year
        age=0
        if record.birthday:
          birth = datetime.strptime(record.birthday, "%Y-%m-%d").year
          age= today - birth
        # age = 0
        # if record.birthday:
        #   age = relativedelta(
        #     fields.Date.today(),
        #     record.birthday,
        #   ).years
        record.age = age