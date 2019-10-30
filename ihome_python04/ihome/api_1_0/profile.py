# -*- coding:utf-8 -*-
from . import api
from flask import request, jsonify, current_app,g, session
from ihome.utils.commons import login_required
from ihome.utils.image_storge import storage
from ihome.utils.response_code import RET
from ihome import constants, db
from ihome.models import User

import sys
reload(sys)
sys.setdefaultencoding('utf8')


@api.route("/users/avatar", methods=["POST"])
@login_required
def set_avatar():
    user_id = g.user_id
    image_file = request.files.get("avatar")
    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")
    image_data = image_file.read()
    try:
        file_name = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")
    try:
        User.query.filter_by(id=user_id).update({"avatar_url": file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片信息失败")

    avatar_url = constants.QINIU_URL_DOMAIN + file_name

    return jsonify(errno=RET.OK, errmsg="上传图片成功", data={"avatar_url": avatar_url})


@api.route("/users/name", methods=["POST"])
@login_required
def change_user_name():
    user_id = g.user_id
    requ_data = request.get_json()
    if not requ_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    user_name = requ_data.get("user_name")
    if not user_name:
        return jsonify(errno=RET.PARAMERR, errmsg="名字不能为空")
    try:
        User.query.filter_by(id=user_id).update({"name": user_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="用户名设置失败")
    session["name"] = user_name
    return jsonify(errno=RET.OK, errmsg="修改用户名成功", data={"name": user_name})


@api.route("/user")
@login_required
def get_user_info():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户失败")
    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")
    return jsonify(errno=RET.OK, errmsg="ok", data={"user": user.to_dict()})


@api.route("/users/auth", methods=["GET"])
@login_required
def get_user_auth():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户失败")
    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")
    return jsonify(errno=RET.OK, errmsg="ok", data=user.auth_to_dict())


@api.route("/users/auth", methods=["POST"])
@login_required
def set_user_auth():
    user_id = g.user_id
    requ_data = request.get_json()
    if not requ_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    real_name = requ_data.get("real_name")
    id_card = requ_data.get("id_card")
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None).update({"real_name": real_name, "id_card": id_card})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="用户认证信息保存失败")
    return jsonify(errno=RET.OK, errmsg="用户认证信息保存成功")
