# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WizardAppointments(models.TransientModel):
    _name = 'appointments.wizard'
    _description = "Wizard: Quick Registration of Appointments "

    patient_id = fields.Many2one('hospital.patients', string='Patients Name')
    appointment_date = fields.Datetime()

    # Create Record From Code
    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created From The Wizard/Code'
        }
        self.patient_id.message_post(body="Test string ", subject="Appointment Creation")
        new_appointment = self.env['hospital.appointments'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointments',
                'res_id': new_appointment.id,
                'context': context
                }

    def print_reports(self):
        data = {
            'model': 'appointments.wizard',
            'form': self.read()[0]
        }
        return self.env.ref('tamam_hospital.report_appointments').with_context(landscape=True).\
            report_action(self, data=data)

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()

    # get data from data base
    def get_data(self):
        appointment = self.env['hospital.appointments'].search([])
        print("appointment", appointment)
        for rec in appointment:
            print("Appointment Name", rec.name)
