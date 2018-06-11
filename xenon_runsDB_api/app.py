import os
from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/run"

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)


def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp


DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS


class Root(Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


api.add_resource(Root, '/')

from xenon_runsDB_api.runs import list, tag 
from xenon_runsDB_api.run import *
