#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from flask_restplus import Api, Resource, fields
from flask import request, g
from werkzeug.datastructures import FileStorage
from wtforms import Form, BooleanField, TextField, validators
from wtforms.validators import Required

from application import app_logic

app = Flask(__name__)
api = Api(app, version='1.0', title='Seed Rocket')
ns = api.namespace('profile', description='Profile operations')

parser = api.parser()
parser.add_argument('email', type=str, location='form', required=True)


def get_response_success(message, status_code):
    return {
        'success': True,
        'message': message
    }, status_code

def get_response_failed(message, errors, status_code):
    return {
        'success': True,
        'message': message,
        'has_validation_errors': True,
        'errors': errors
    }, status_code

@ns.route('/')
class Profile(Resource):
    @api.doc(parser=parser)
    def post(self):
        req_form = self.ProfileForm(request.form)

        if req_form.validate():
            email = request.form['email']

            success, message = app_logic.try_subscribe(email)
            if success:
                return get_response_success(message=message, status_code=201)
            return get_response_failed(message=message, errors={}, status_code=400)
        return get_response_failed(message='subscription_failed', errors=req_form.errors, status_code=400)

    class ProfileForm(Form):
        email = TextField('email', [
            Required(message='email_field_cannot_be_empty'),
            validators.Email(message="email_not_valid")])

if __name__ == '__main__':
    app.run(debug=True)
