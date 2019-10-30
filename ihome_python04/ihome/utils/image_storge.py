# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_data, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'QNLiGtRQrI3J_KHpBKJe49vPDo9bNud8WeT5j-LP'
secret_key = 'S4RH25LTFKsVtk4CMFco2ernAjcjdX50M2vBHNAK'


def storage(file_data):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'ihome_new'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    ret, info = put_data(token, None, file_data)
    if info.status_code == 200:
        return ret.get("key")
    else:
        raise Exception("上传图片失败")


