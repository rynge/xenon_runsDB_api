from flask_restful import Resource
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
    def _get_(self, key, value):
        app.logger.debug("Requesting data for run with %s %s"
                         % (key, value))
        result = mongo.db["runs_new"].find_one_or_404(
            {key: value}, 
            {"data": 1, "name": 1, "_id": 1, "number": 1})
        app.logger.debug("Keys for result: %s" % result.keys())
        return flask.jsonify({"results": result})
    
    def _put_normal_data_(self, key, value, data):

    @use_kwargs(data_raw_args, locations=["json"])
    def _put_raw_data_(self):


class RunObjectIDData(RunData):
    def get(self, object_id):
        return self._get_("object_id", object_id)


class RunRunNumberData(RunData):
    def get(self, run_number):
        return self._get_("number", run_number)


class RunTimestampData(RunData):
    def get(self, timestamp):
        return self._get_("name", timestamp)


class RunDataRaw(Resource):
    def _put_(self, location):
        if data_type:
            query = {"data": {"$elemMatch": {"type": data_type,
                                             "rse": location}}}
        else:
            query = {"data": {"$elemMatch": {"rse": location}}}
        results = util.get_data_single_top_level(query, data_field)
        app.logger.debug("results: %s" % results)
        return results



api.add_resource(RunsLocationList,
                 '/run/objectid/<ObjectId:object_id>/data/',
                 endpoint="run_object_id_data")
api.add_resource(RunsLocationList,
                 '/runs/objectid/<ObjectId:object_id>/data/',
                 endpoint="runs_object_id_data")

api.add_resource(RunRunNumberData,
                 '/run/runnumber/<int:run_number>/data/',
                 endpoint="run_run_number_data")
api.add_resource(RunRunNumberData,
                 '/run/number/<int:run_number>/data/',
                 endpoint="run_number_data")
api.add_resource(RunRunNumberData,
                 '/runs/runnumber/<int:run_number>/data/',
                 endpoint="runs_run_number_data")
api.add_resource(RunRunNumber,
                 '/runs/number/<int:run_number>/data/',
                 endpoint="runs_number_data")

api.add_resource(RunTimestampData,
                 '/run/timestamp/<string:timestamp>/data/',
                 endpoint="run_timestamp_data")
api.add_resource(RunTimestampData,
                 '/run/name/<string:timestamp>/data/',
                 endpoint="run_name_timestamp_data")
api.add_resource(RunTimestampData,
                 '/runs/timestamp/<string:timestamp>/data/',
                 endpoint="runs_timestamp_data")
api.add_resource(RunTimestampData,
                 '/runs/name/<string:timestamp>/data/',
                 endpoint="runs_name_timestamp_data")