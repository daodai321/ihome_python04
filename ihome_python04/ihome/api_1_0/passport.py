# -*- coding:utf-8 -*-

from . import api
from flask import request, current_app, session, jsonify
from ihome.utils.response_code import RET
from ihome import db, redis_store,constants
from ihome.models import User
from sqlalchemy.exc import IntegrityError
import re
from werkzeug.security import generate_password_hash, check_password_hash


@api.route("/users", methods=["POST"])
def register():
    # 获取手机号,短信验证码,密码
    requ_dict = request.get_json()
    mobile = requ_dict.get("mobile")
    sms_code = requ_dict.get("sms_code")
    password = requ_dict.get("password")
    password2 = requ_dict.get("password2")
    # 手机号和短信验证码的校验
    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="数据不完整")
    if not re.match(r"1[35689]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式不正确")
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")
    # 判断短信验证码是否正确
    try:
        real_sms_code = redis_store.get(mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis查询错误")
    else:
        if real_sms_code != sms_code:
            return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")
    # 判断手机有没有被注册过
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    # else:
    #     if user is not None:
    #         return jsonify(errno=RET.DATAEXIST, errmsg="用户已注册")

    # 把手机号保存为user类的对象
    user = User(mobile=mobile, name=mobile)
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="用户已注册")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    # 保存用户登陆状态
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route("/sessions", methods=["POST"])
def login():
    requ_dict = request.get_json()
    mobile = requ_dict.get("mobile")
    password = requ_dict.get("password")
    # 校验手机号和密码
    if not all([mobile, password]):
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="数据不完整")
    if not re.match(r"1[3578]\d{9}", mobile):
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式不正确")

    # 判断用户名是否已经存在
    user_ip = request.remote_addr
    try:
        assess_num = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if assess_num is not None and assess_num >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="登陆错误次数过多,请稍后再试")
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    if user is None or not check_password_hash(user.password_hash,password):
        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg="登录成功")


@api.route("/session", methods=["GET"])
def check_login():
    name = session.get("name")
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    csrf_token = session.get("csrf_token")
    session.clear()
    session["csrf_token"] = csrf_token
    return jsonify(errno=RET.OK, errmsg="OK")























