import os
import json
import flask
from datetime import datetime
from flask import url_for
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.json_util import dumps

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/run"

app = flask.Flask(__name__)
app.json_encoder = JSONEncoder

app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)


def output_json(obj, code, headers=None):
    resp = flask.make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp


DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

from xenon_runsDB_api.runs import status, list, tag, query, detector, location
from xenon_runsDB_api.run import run, gains, data

class Root(Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


api.add_resource(Root, '/')

class SiteMap(Resource):
    def get(self):
        return flask.jsonify(
            {"routes": ['%s' % rule for rule in app.url_map.iter_rules()]})


api.add_resource(SiteMap, '/sitemap')
