import logging

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
