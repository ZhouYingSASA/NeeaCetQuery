from flask import Flask
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from .utils.redis_config import passportRedis
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
auth = HTTPTokenAuth('...')
inner_auth = HTTPBasicAuth()
rds = passportRedis()


def create_app(config_name):
    app = Flask(__name__)
    cfg = config[config_name]

    app.config.from_object(cfg)
    cfg.init_app(app)

    db.init_app(app)
