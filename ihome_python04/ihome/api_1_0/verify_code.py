# coding:utf-8
from flask import make_response, current_app, jsonify, request
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import constants, redis_store
from ihome.utils.response_code import RET
from ihome.libs.yuntongxun.SendTemplateSMS import CCP
import random
from ihome.models import User


@api.route("/image_codes/<image_code_id>", methods=["GET"])
def get_image_code(image_code_id):
    # 业务处理
    # 生成验证码
    name, text, image_data = captcha.generate_captcha()
    # 1.获取验证码图片和id
    # 2.将两者存进redis并设置有效期
    try:
        redis_store.setex("image_code_%s"%image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="保存图片验证码失败")
    # 返回
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


@api.route("/sms_codes/<re(r'1[3578]\d{9}'):mobile>")
def get_sms_code(mobile):
    # 获取图片验证码
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    # 判断数据完整性
    if not all([image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="数据不完整")
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis查询异常")
    if not real_image_code:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 在对比之前删除redis中的验证码,防止验证码重复使用
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 防止在短时间内多次发送短信验证码
    try:
        send_flag = redis_store.get("send_sms_code_%s" % sms_code)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="请求次数过于频繁,请60秒之后重试")
    # 获取短信验证码之前判断图片验证码
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
    # 判断用户手机是否已经注册
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg="用户账号已存在")

    # 生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)
    # 保存短信验证码
    try:
        redis_store.setex(mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        redis_store.setex("send_sms_code_%s" % sms_code, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")
    # 发送短信验证码
    ccp = CCP()
    try:
        ccp.send_templatesms("sms_code_%s" % mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="发送失败")
    # 返回
    return jsonify(errno=RET.OK, errmsg="发送成功")




