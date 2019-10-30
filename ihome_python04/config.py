# coding: utf-8
import redis


class Config():
    SECRET_KEY = "SDKJFHKLGJ@G544H"
    # sqlalchemy设置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome_python04"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis设置
    REDIS_HOST = "127.0.0.1"
    REDIS_POST = 6379
    # session设置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_POST)
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发者的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产者的配置信息"""
    pass

config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
              }