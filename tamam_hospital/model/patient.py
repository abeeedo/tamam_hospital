# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatients(models.Model):
    _name = 'hospital.patients'
    _description = 'Patients Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_name'

    name = fields.Char(string="Contact Number")
    patient_name = fields.Char(string='Patient Name', required=True)
    patient_age = fields.Integer(string='Patient Age', track_visibility="always", group_operator=False)
    email_id = fields.Char(string='Email')
    notes = fields.Text('Registration Notes')
    user_id = fields.Many2one('res.users', string="PRO")
    image = fields.Binary(string="Image", attachment=True)
    name_seq = fields.Char(string='Patient IDs', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    patient_name_upper = fields.Char(
        compute='_compute_upper_name', inverse='_inverse_upper_name',
                                     help='for capitalize letters')
    gender = fields.Selection([('male', 'Male'), ('fe_male', 'Female')], string="Gender", default='male')
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string="Age Group", compute='set_age_group', store=True)
    active = fields.Boolean('Active', default=True)
    doctor_id = fields.Many2one('hospital.doctors', string='Doctor')
    doctor_gender = fields.Selection([('male', 'Male'), ('fe_male', 'Female')],
                                     string="Doctor Gender")
    pharmacy_note = fields.Text(string='Pharmacy Note')
    description_note = fields.Text(string='Description Note')
    email_id = fields.Char(string="Email")

    # call python from menu
    def action_patients(self):
        print('ggggggggggggggg')
        return {
            'name': _('Patients Server Action'),
            'domain': [],
            'view_type': 'form',
            'res_model': 'hospital.patients',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    # cron job
    def test_crons_job(self):
        for rec in self:
            print('Abcd', rec)

    # Overriding the create method to assign sequence for the record
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patients.sequence') or _('New')
        result = super(HospitalPatients, self).create(vals)
        return result

    # name get function for the model executes automatically
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.patient_name, rec.name_seq)))
        return res

    # report from button
    def print_reports(self):
        return self.env.ref('tamam_hospital.report_patients_view_card').report_action(self)

    # onchange
    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.genders

    # related field
    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    # Add Constrains For a Field
    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age < 5:
                raise ValidationError(_('The Age Must be Greater Than 5..!'))

    # computed field
    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    # computed field editable
    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    # sequence
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('Tamam.patient.sequence') or _('New')
        result = super(HospitalPatients, self).create(vals)
        return result

    # button_test
    def button_test(self):
        for rec in self:
            # patients_count = self.env['hospital.patients'].search_count([])
            # print("eeeeeeeeeeeeeeeeeeee....", patients_count)

            # # search
            female_patients = self.env['hospital.patients'].search([('gender', '=', 'fe_male')])
            print("lllllllllllll....", female_patients)

            # product_category = self.env['product.category'].search([]).mapped('name')
            # print("lllllllllllll....", product_category)
            #
            # product_category_context = self.env['product.category'].with_context(lang='ar_SY').search([]).mapped('name')
            # print("lllllllllllll....", product_category_context)
            #
            # patients = self.env['hospital.patients'].search([])
            # print("lllllllllllll....", patients)
            #
            # filtered_female_patients = self.env['hospital.patients'].search([]).filtered(lambda s: s.gender ==
            # 'fe_male') print("lllllllllllll....", filtered_female_patients)
            #
            # mapped_female_patients = self.env['hospital.patients'].search([]).sorted(key='patient_age',
            # reverse=True).mapped('patient_age') print("lllllllllllll....", mapped_female_patients)

            # reference
            # om_paitent = self.env.ref('tamam_hospital.patients_xyz')
            # print('om_paitent', om_paitent.id)

            # browse
            # browse_result = self.env['hospital.patients'].browse(20)
            # browse_result = self.env['hospital.patients'].search([('id', '=', 20)])
            # print('browse_result...', browse_result)

            # if browse_result.exists():
            #     print("existing")
            # else:
            #     print("Nooooooooooooooooooooo")

            # create
            # vals = {
            #     'patient_name': 'Sajd',
            # }
            # created_record = self.env['hospital.patients'].create(vals)
            # print('uuuuuuuuuuuuuuuu...', created_record, created_record.id)
            #
            # browse_result = self.env['hospital.patients'].browse(20)
            # if browse_result.exists:
            #     vals = {
            #         'patient_age': '48',
            #         'notes': 'I Hope This Find You Will'
            #     }
            #     browse_result.write(vals)
            # browse_result = self.env['hospital.patients'].browse(22)
            # browse_result.unlink()

    # Sending Email in Button Click
    # def action_send_card(self):
    #     # sending the patient report to patient via email
    #     template_id = self.env.ref('tamam_hospital.patients_cards_email_template').id
    #     template = self.env['mail.template'].browse(template_id)
    #     template.send_mail(self.id, force_send=True)


class SaleOrderInherits(models.Model):
    _inherit = 'sale.order'

    # Inheriting the Sale Order Model and Adding New Field
    names = fields.Char(string='Patients Names')

    # OverRide Create Method Of a Model
    def action_confirm(self):
        res = super(SaleOrderInherits, self).action_confirm()
        print('yes working ----------!!!!!!!!')
        return res


class ResPartnerss(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('plus', 'Plus')])

    @api.model
    def create(self, vals_list):
        res = super(ResPartnerss, self).create(vals_list)
        print("Yes Working !!!!!!!!!!!!!!!!!!!!")
        return res



