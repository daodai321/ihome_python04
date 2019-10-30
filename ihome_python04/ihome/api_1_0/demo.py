# coding:utf-8

from . import api
from ihome import db,models
from flask import current_app


@api.route("/index")
def index():
    current_app.logger.error("ok")
    return "index_page"