from flask_restful import Resource
from webargs import fields
from xenon_runsDB_api import util
from xenon_runsDB_api.app import app, api


data_normal_args = {
    "checksum": fields.String(required=True),
    "creation_place": fields.String(required=True),
    "creation_time": fields.DateTime(format="iso", required=True),
    "host": fields.String(required=True),
    "location": fields.String(required=True),
    "pax_version": fields.String(required=True),
    "status": fields.String(required=True),
    "type": fields.String(required=True)
    }

data_raw_args = {
    "checksum": fields.String(required=True),
    "creation_time": fields.DateTime(required=True, format="iso"),
    "host": fields.String(required=True),
    "location": fields.String(required=True),
    "rse": fields.List(fields.String(required=True)),
    "rule_info": fields.List(fields.String(required=True)),
    "status": fields.String(),
    "type": fields.String()
    }


class RunData(Resource):
    def _get_(self, key, value, data_type=None):
        app.logger.debug("Requesting data for run with %s %s"
                         % (key, value))
        result = mongo.db["runs_new"].find_one_or_404(
            {key: value}, 
            {"data": 1, "name": 1, "_id": 1, "number": 1}
        )
        print(results)
        app.logger.debug("Keys for result: %s" % result.keys())
        return result
    
    def _post_normal_data_(self, key, value, data):
        run_doc_before = mongo.db["runs_new"].find_one_or_404(
            {key: value})
        mongo.db["runs_new"].find_one_and_update(
            {key: value},
            {"$push": {"data": data}}
        )
        run_doc_after= mongo.db["runs_new"].find_one_or_404(
            {key: value})
        return flask.jsonify({"previous_run_doc": run_doc_before,
                              "new_run_doc": run_doc_after})
        
    def _post_raw_data_(self, key, value, data):
        pass


class RunObjectIDData(RunData):
    def get(self, object_id, data_type=None):
        if not data_type:
            result = self._get_("object_id", object_id)
            return flask.jsonify({results: result})
        else:
            pass


class RunRunNumberData(RunData):
    def get(self, run_number, data_type=None):
        if not data_type:
            result = self._get_("number", run_number)
            return flask.jsonify({results: result})
        else:
            pass

class RunTimestampData(RunData):
    def get(self, timestamp, data_type=None):
        print(timestamp)
        if not data_type:
            result = self._get_("name", timestamp)
            return flask.jsonify({results: result})
        else:
            pass

api.add_resource(RunObjectIDData,
                 '/run/objectid/<ObjectId:object_id>/data/'
                 '/run/objectid/<ObjectId:object_id>/data/<string:data_type>/',
                 endpoint="run_object_id_data")
api.add_resource(RunObjectIDData,
                 '/runs/objectid/<ObjectId:object_id>/data/',
                 '/runs/objectid/<ObjectId:object_id>/data/<string:data_type>/',
                 endpoint="runs_object_id_data")

api.add_resource(RunRunNumberData,
                 '/run/runnumber/<int:run_number>/data/<string:data_type>/',
                 endpoint="run_run_number_data")
api.add_resource(RunRunNumberData,
                 '/run/number/<int:run_number>/data/<string:data_type>/',
                 endpoint="run_number_data")
api.add_resource(RunRunNumberData,
                 '/runs/runnumber/<int:run_number>/data/<string:data_type>/',
                 endpoint="runs_run_number_data")
api.add_resource(RunRunNumberData,
                 '/runs/number/<int:run_number>/data/<string:data_type>/',
                 endpoint="runs_number_data")

api.add_resource(RunTimestampData,
                 '/run/timestamp/<string:timestamp>/data/<string:data_type>/',
                 endpoint="run_timestamp_data")
api.add_resource(RunTimestampData,
                 '/run/name/<string:timestamp>/data/<string:data_type>/',
                 endpoint="run_name_timestamp_data")
api.add_resource(RunTimestampData,
                 '/runs/timestamp/<string:timestamp>/data/<string:data_type>/',
                 endpoint="runs_timestamp_data")
api.add_resource(RunTimestampData,
                 '/runs/name/<string:timestamp>/data/<string:data_type>/',
                 endpoint="runs_name_timestamp_data")

