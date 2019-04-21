from flask import Blueprint

api = Blueprint('api_1_0', __name__, url_prefix='/api_1_0')

from .verify_code import get_image_code, send_sms_code