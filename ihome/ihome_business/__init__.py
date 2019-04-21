from flask import Flask
from config import config_map, Config
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
import logging
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
from .util.common import ReConverter
from web_html import html

db = SQLAlchemy()

redis_store = None

# 配置日志信息
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_map.get('develop'))
    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(Config.REDIS_HOST, Config.REDIS_PORT)
    Session(app)
    CSRFProtect(app)
    from ihome_business.api_1_0 import api
    app.url_map.converters['re'] = ReConverter
    app.register_blueprint(api)
    app.register_blueprint(html)
    return app


