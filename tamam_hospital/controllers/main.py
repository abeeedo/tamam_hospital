from odoo import http
from odoo.http import request


class AppointmentController(http.Controller):

    # sample controller created
    @http.route('/tamam_hospital/patients/', website=True, auth="user")
    def hospital_patients(self, **kw):
        # return "Thanks For Watching"
        patients = request.env['tamam_hospital.create_patient.patients'].sudo().search([])
        print('patients...', patients)
        return request.render("tamam_hospital.patients_pages", {
            'patients': patients
        })


class AppointmentController(http.Controller):

    @http.route('/tamam_hospital/appointments', auth='user', type='json')
    def appointment_banner(self):
        return {
            'html': """
                    <div>
                        <link>
                        <center><h1><font color="red">Subscribe our channel.......!</font></h1></center>
                        <center>
                        <p><font color="blue"><a href="https://www.youtube.com">
                            Get Notified Regarding All The Odoo Updates!</a></p>
                            </font></div></center> """
        }

class Hospital(http.Controller):

    @http.route('/patient_webform', type="http", auth="public", website=True)
    def patient_webform(self, **kw):
        print("Execution Here.........................")
        doctor_rec = request.env['hospital.doctors'].sudo().search([])
        print("doctor_rec...", doctor_rec)
        return http.request.render('tamam_hospital.create_patient', {'patient_name': 'Odoo Mates Test 123',
                                                                  'doctor_rec': doctor_rec})

    @http.route('/create/webpatient', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):
        print("Data Received.....", kw)
        request.env['hospital.patients'].sudo().create(kw)
        # doctor_val = {
        #     'name': kw.get('patient_name')
        # }
        # request.env['hospital.doctor'].sudo().create(doctor_val)
        return request.render("tamam_hospital.patient_thanks", {})


