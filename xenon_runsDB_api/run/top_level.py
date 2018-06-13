from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo


class RunTopLevelObjectID(Resource):
    def get(self, object_id, top_level):
        app.logger.debug("Requesting data for run with object ID %s"
                         % object_id)
        result = mongo.db.runs_new.find_one_or_404({"_id": object_id})
        return result[top_level]


class RunTopLevelRunID(Resource):
    def get(self, run_id, top_level):
        app.logger.debug("Requesting data for run with run number %s"
                         % run_id)
        result = mongo.db.runs_new.find_one_or_404({"number": run_id})
        return result[top_level]


class RunTopLevelTimestamp(Resource):
    def get(self, timestamp, top_level):
        app.logger.debug("Requesting data for run with timestamp %s"
                         % timestamp)
        result = mongo.db.runs_new.find_one_or_404({"name": timestamp})
        return result[top_level]


api.add_resource(RunTopLevelObjectID,
                 '/run/objectid/<ObjectId:object_id>/<string:top_level>/',
                 endpoint="run_object_id_toplevel")
api.add_resource(RunTopLevelRunID,
                 '/run/runnumber/<int:run_id>/<string:top_level>/',
                 endpoint="run_run_id_toplevel")
api.add_resource(RunTopLevelTimestamp,
                 '/run/timestamp/<string:timestamp>/<string:top_level>/',
                 endpoint="run_timestamp_toplevel")

api.add_resource(RunTopLevelObjectID,
                 '/runs/objectid/<ObjectId:object_id>/<string:top_level>/',
                 endpoint="runs_object_id_toplevel")
api.add_resource(RunTopLevelRunID,
                 '/runs/runnumber/<int:run_id>/<string:top_level>/',
                 endpoint="runs_run_id_toplevel")
api.add_resource(RunTopLevelTimestamp,
                 '/runs/timestamp/<string:timestamp>/<string:top_level>/',
                 endpoint="runs_timestamp_toplevel")
