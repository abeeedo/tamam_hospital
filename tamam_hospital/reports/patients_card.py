from odoo import api, models, _


class PatientsCardReport(models.AbstractModel):
    _name = 'report.tamam_hospital.report_patients_views'
    _description = 'Patients card Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hospital.patients'].browse(docids[0])
        appointments = self.env['hospital.appointments'].search([('patient_id', '=', docids[0])])
        appointment_list = []
        for app in appointments:
            vals = {
                'name': app.name,
                'notes': app.notes,
                'appointment_date': app.appointment_date
            }
            appointment_list.append(vals)
        return {
            'doc_model': 'hospital.patients',
            'docs': docs,
            'appointment_list': appointment_list,
        }