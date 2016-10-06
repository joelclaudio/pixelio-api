from application.api import api
from flask_restplus import fields

def response_success(message="", data=None, status_code=200):
    return {'success': True,
            'message': message,
            'data': data
            }, status_code

def response_failed(message="", errors=None, has_validation_errors=False, status_code=400):
    return {'success': False,
            'message': message,
            'errors': errors,
            'has_validation_errors': has_validation_errors
            }, status_code