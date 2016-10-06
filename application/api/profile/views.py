from application import app
from application.api import api
from flask import Flask, url_for
from flask_restplus import Resource
from application.api.utils import response_models
from flask import request, g

from wtforms import Form, BooleanField, TextField, validators
from wtforms.validators import Required

from application.api import ns_profile
from application.api.profile import logic

@ns_profile.route('/<string:mac_address>', endpoint='self')
class Profile(Resource):
    def get(self, mac_address):
        success, message, data, created = logic.get_profile_by_mac_address(mac_address)
        if success:
            return response_models.response_success(message=message, data=data, status_code=200 if not created else 201)
        return response_models.response_failed(message=message, status_code=400)

profile_form = api.parser()
profile_form.add_argument(
    'mac_address', type=str, help='Enter Mac Address', location='form')

@ns_profile.route('/', endpoint='manage_profile')
class ManageProfile(Resource):
    @api.doc(parser=profile_form)
    def post(self):
        req_form = self.Profile(request.form)
        if req_form.validate():
            mac_address = request.form['mac_address']
            success, message, data = logic.create_profile(mac_address)
            if success:
                return response_models.response_success(message=message, data=data, status_code=201)
            return response_models.response_failed(message=message, status_code=400)
        return response_models.response_failed('bad_parameters', errors=req_form.errors, has_validation_errors=True, status_code=400)
        

    class Profile(Form):
        mac_address = TextField('mac_address', [
            Required(message='email_field_cannot_be_empty')
        ])
    