from flask import Flask, url_for
from flask_restplus import Api, Resource
from flask import Blueprint


app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

from application.api import api_blueprint
app.register_blueprint(api_blueprint)

from flask.ext.restplus import apidoc
@app.route('/doc/', endpoint='doc')
def swagger_ui():
    from application.api import api
    return apidoc.ui_for(api)



