import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# swagger code
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'BYR': "BYR api"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# adding the logger to the app
logging.basicConfig(filename='./logs/record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')


# @app.before_first_request
# def before_first_request():
#     log_level = logging.INFO

#     for handler in app.logger.handlers:
#         app.logger.removeHandler(handler)

#     handler = logging.FileHandler('./logs/record.log')
#     handler.setLevel(log_level)
#     app.logger.addHandler(handler)

#     app.logger.setLevel(log_level)
