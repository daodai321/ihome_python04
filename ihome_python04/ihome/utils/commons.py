# coding: utf-8
from werkzeug.routing import BaseConverter
from flask import session, g, jsonify
import functools


# 定义正则转换器
class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(ReConverter, self).__init__(url_map)
        self.regex = regex


# 定义登录装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id is not None:
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return wrapper
