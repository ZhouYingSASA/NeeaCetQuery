# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from .resources.cet import Cet, Zkzh

cet_blueprint = Blueprint("cet", __name__)

cet_api = Api(cet_blueprint)
cet_api.add_resource(Cet, "/result")
cet_api.add_resource(Zkzh, "/zkzh")
