import flask
import flask_praetorian
from flask_restful import Resource
from marshmallow import Schema, fields
from webargs.flaskparser import use_kwargs, use_args
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api, mongo, config
from collections import defaultdict


class RunRucio(Resource):

    def __init__(self):
        self.mongodb = mongo.db[config["runsDB"]["database_name"]]
        self.views = {"data": 1}
        self.views.update(config["runsDB"]["views"]["limited_view"])

    def _get_(self, key, value, data_type=None):
        """
        
        """
        app.logger.debug("Requesting data for run with %s %s"
                         % (key, value))
        app.logger.debug("views %s" % self.views)
        result = self.mongodb.find_one_or_404({key: value}, self.views)
        app.logger.debug("Query results: %s", result)
        if data_type:
            limited_data = [do["location"] for do in result["data"] 
                            if do["type"] == data_type]
            result["dids"] = {}
            result["dids"][data_type] = limited_data
        else:
            d = defaultdict(list)
            for do in result["data"]:
                d[do["type"]].append(do["location"])
            result["dids"] = d
        result.pop("data")
        app.logger.debug("Keys for result: %s" % result.keys())
        return result


class RunObjectIDRucio(RunRucio):
    def get(self, object_id, data_type=None):
        result = self._get_("object_id", object_id, data_type)
        return flask.jsonify({"results": result})


class RunRunNumberRucio(RunRucio):
    def get(self, run_number, data_type=None):
        result = self._get_("number", run_number, data_type)
        return flask.jsonify({"results": result})


class RunTimestampRucio(RunRucio):
    def get(self, timestamp, data_type=None):
        result = self._get_("name", timestamp, data_type)
        return flask.jsonify({"results": result})


api.add_resource(RunObjectIDRucio,
                 '/run/objectid/<ObjectId:object_id>/data/dids',
                 endpoint="run_did_object_id_data_no_type")
api.add_resource(RunObjectIDRucio,
                 ('/run/objectid/<ObjectId:object_id>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="run_did_object_id_data",
                 methods=['GET'])

api.add_resource(RunObjectIDRucio,
                 '/runs/objectid/<ObjectId:object_id>/data/dids',
                 endpoint="runs_did_object_id_data_no_type")
api.add_resource(RunObjectIDRucio,
                 ('/runs/objectid/<ObjectId:object_id>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="runs_did_object_id_data",
                 methods=['GET'])


api.add_resource(RunRunNumberRucio,
                 '/run/number/<int:run_number>/data/dids',
                 endpoint="run_did_number_data_no_type")
api.add_resource(RunRunNumberRucio,
                 ('/run/number/<int:run_number>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="run_did_number_data",
                 methods=['GET'])

api.add_resource(RunRunNumberRucio,
                 '/run/runnumber/<int:run_number>/data/dids',
                 endpoint="run_did_run_number_data_no_type")
api.add_resource(RunRunNumberRucio,
                 ('/run/runnumber/<int:run_number>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="run_did_run_number_data",
                 methods=['GET'])       

api.add_resource(RunRunNumberRucio,
                 '/runs/number/<int:run_number>/data/dids',
                 endpoint="runs_did_number_data_no_type")
api.add_resource(RunRunNumberRucio,
                 ('/runs/number/<int:run_number>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="runs_did_number_data",
                 methods=['GET'])

api.add_resource(RunRunNumberRucio,
                 '/runs/runnumber/<int:run_number>/data/dids',
                 endpoint="runs_did_run_number_data_no_type")
api.add_resource(RunRunNumberRucio,
                 ('/runs/runnumber/<int:run_number>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="runs_did_run_number_data",
                 methods=['GET'])


api.add_resource(RunTimestampRucio,
                 '/run/timestamp/<string:timestamp>/data/dids',
                 endpoint="run_did_timestamp_data_no_type")
api.add_resource(RunTimestampRucio,
                 ('/run/timestamp/<string:timestamp>'
                  '/data/<string:data_type>/'),
                 endpoint="run_did_timestamp_data",
                 methods=['GET'])

api.add_resource(RunTimestampRucio,
                 '/run/name/<string:timestamp>/data/dids',
                 endpoint="run_did_name_timestamp_data_no_type")
api.add_resource(RunTimestampRucio,
                 ('/run/name/<string:timestamp>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="run_did_name_timestamp_data",
                 methods=['GET'])

api.add_resource(RunTimestampRucio,
                 '/runs/timestamp/<string:timestamp>/data/dids',
                 endpoint="runs_did_timestamp_data_no_type")
api.add_resource(RunTimestampRucio,
                 ('/runs/timestamp/<string:timestamp>'
                  '/data/<string:data_type>/'),
                 endpoint="runs_did_timestamp_data",
                 methods=['GET'])

api.add_resource(RunTimestampRucio,
                 '/runs/name/<string:timestamp>/data/dids',
                 endpoint="runs_did_name_timestamp_data_no_type")
api.add_resource(RunTimestampRucio,
                 ('/runs/name/<string:timestamp>'
                  '/data/dids/<string:data_type>/'),
                 endpoint="runs_did_name_timestamp_data",
                 methods=['GET'])