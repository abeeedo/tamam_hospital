# -*- coding: utf-8 -*-

import pytz
from odoo import models, fields, api, _


class HospitalAppointments(models.Model):
    _name = 'hospital.appointments'
    _description = 'Appointments for Patients'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "appointment_date asc"

    patient_id = fields.Many2one('hospital.patients', string='Patient', required=True)
    name = fields.Char(string='Appointment ID')
    appointments_lines = fields.One2many('hospital.appointments.lines', 'appointments_id', string='Appointment Lines')
    pharmacy_note = fields.Char()
    appointment_date = fields.Datetime(string='Date Time')
    appointment_date_end = fields.Datetime(string='End Date Time')
    doctor_id = fields.Many2one('hospital.doctors', string='Doctor')
    doctor_ids = fields.Many2many('hospital.doctors', string='Doctors')
    notes = fields.Char('Notes')
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    partner_id = fields.Many2one('res.partner', string='Customer')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    amount = fields.Float(string="Total Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')
    product_id = fields.Many2one('product.product', string="Product Template")

    # default get data
    # @api.model
    # def default_get(self, fields):
    #     res = super(HospitalAppointments, self).default_get(fields)
    #     appointment_lines = []
    #     product_rec = self.env['product.product'].search([])
    #     for pro in product_rec:
    #         line = (0, 0, {
    #             'product_id': pro.id,
    #             'product_qty': 1,
    #         })
    #         appointment_lines.append(line)
    #     res.update({
    #         'appointment_lines': appointment_lines,
    #         'patient_id': 1,
    #         'notes': 'Please Like and Subscribe our channel To Get Notified'
    #     })
    #     return res

    # # one2many update onchange
    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     for rec in self:
    #         lines = [(5, 0, 0)]
    #         print('self.product_id', self.product_id.product_variant_ids)
    #         for line in self.product_id.product_variant_ids:
    #             vals = {
    #                 'product_id': line.id,
    #                 'product_qty': 5
    #             }
    #             lines.append((0, 0, vals))
    #         print('lines', lines)
    #         rec.appointments_lines = lines

    # How To Give Domain For A Field Based On Another Field
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_warning("Appointment is Confirmed")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed... Thanks You',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = 'draft'

    # report from button
    def print_reports(self):
        return self.env.ref('tamam_hospital.report_appointments').report_action(self)

    # default get
    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointments, self).default_get(fields)
        print('testttttt ..................')
        res['patient_id'] = 1
        res['pharmacy_note'] = 'Like and Subscribe our channel To Get Notified'
        return res

    # override write function
    def write(self, vals):
        res = super(HospitalAppointments, self).write(vals)
        print('test write ')
        return res

    # delete lines from a button
    def delete_lines(self):
        for rec in self:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            time_in_timezone = pytz.utc.localize(rec.appointment_date).astimezone(user_tz)
            print("Time in UTC -->", rec.appointment_date)
            print("Time in Users Timezone -->", time_in_timezone)
            rec.appointments_lines = [(5, 0, 0)]


class HospitalAppointmentsLines(models.Model):
    _name = 'hospital.appointments.lines'

    product_id = fields.Many2one('product.product', string="Medicine")
    product_qty = fields.Integer(string='Quantity')
    sequence = fields.Integer(string='Sequence')
    appointments_id = fields.Many2one('hospital.appointments', string='Appointment ID')
