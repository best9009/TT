from . import api
from ihome_business.util.captcha.captcha import captcha
from ihome_business.util.response_code import RET
from flask import make_response, current_app, jsonify, request
from ihome_business import redis_store
from ihome_business.constants import VERIFY_CODE_MAX_TIME, SMS_CODE_MAX_TIME, SMS_MOBILE_MAX_TIME
from ihome_business.models import User
import random

@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    name, text, image_data = captcha.generate_captcha()
    #print(text)
    try:
        redis_store.setex('image_code_%s'%image_code_id, VERIFY_CODE_MAX_TIME, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库错误')
    #code = redis_store.get('image_code_1')
    #print('****%s*****'%code)
    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp

@api.route('/sms_code/<re(r"1[34578]\d{9}"):mobile>')
def send_sms_code(mobile):
    image_code = request.args.get('image_code')
    image_code_id = request.args.get('image_code_id')
    #print(image_code.lower())
    if not all([image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    try:
        redis_image_code = redis_store.get('image_code_%s'%image_code_id)
        redis_store.delete('image_code_%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库一场')
    if redis_image_code is None:
        return jsonify(errno=RET.PARAMERR, errmsg='验证码国企')

    #print(redis_image_code.decode().lower())
    if image_code.lower() != redis_image_code.decode().lower():
        return jsonify(errno=RET.PARAMERR, errmsg='验证码错误')
    try:
        sms_phone = redis_store.get('sms_phone_%s'%mobile)
    except Exception as e:
        current_app.logger.error(e)
    if sms_phone is not None:
        return jsonify(errno=RET.REQERR, errmsg='请求过于频繁')
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库一场')
    if user is not None:
        return jsonify(errno=RET.DATAEXIST, errmsg='用户手机号已经注册')
    sms_code = "%06d" % random.randint(0, 999999)
    print(sms_code)
    try:
        redis_store.setex('sms_code_%s'%mobile, SMS_CODE_MAX_TIME, sms_code)
        redis_store.setex('sms_phone_%s'%mobile, SMS_MOBILE_MAX_TIME, mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库一场')
    #发送短信

    return jsonify(errno=RET.OK, errmsg='请求成功')
