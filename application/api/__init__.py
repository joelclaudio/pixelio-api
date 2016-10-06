from flask import Blueprint
from flask_restplus import Api, Resource
from flask import make_response

api_blueprint = Blueprint('api_blueprint', __name__)
api = Api(api_blueprint, version='1.0', title='Pixelio-API')

ns_profile = api.namespace('profile', description='Profile operations')

from application.api.profile import views as profile_views


@api_blueprint.after_request
def per_request_callbacks(response):
    try:
        response_json = json.loads(response.data)
    except Exception:
        return response

    resp = make_response(response_json, response.status)
    resp.mimetype = 'application/json'
    return resp