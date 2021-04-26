# -*- coding: utf-8 -*-

from odoo import models, fields


class HospitalDoctors(models.Model):
    _name = 'hospital.doctors'
    # _rec_name = 'name'
    # _description = 'New Description'

    name = fields.Char(string='Name', required=True)
    genders = fields.Selection([('male', 'Male'), ('fe_male', 'Female'), ], default='male', string='Gender')
    user_id = fields.Many2one('res.users', string='Related User')
    appointment_ids = fields.Many2many('hospital.appointments', string='Appointments')
    state = fields.Selection([('draft', 'Draft'), ('check', 'Check Sample'), ('approve', 'Approve'),
                              ('reject', 'Reject')], string='State', default='draft')

    def button_check_sample(self):
        self.write({'state': 'check'})

    def button_approve(self):
        self.write({'state': 'approve'})

    def button_reject(self):
        self.write({'state': 'reject'})



