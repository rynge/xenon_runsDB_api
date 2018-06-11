from flask_restful import Resource
from xenon_runsDB_api import app, api, mongo
from bson.json_util import dumps


class RunDataObjectID(Resource):
    def get(self, object_id):
        app.logger.debug("Requesting data for run with object ID %s"
                         % object_id)
        result = mongo.db.runs_new.find_one_or_404({"_id": object_id})
        return result["data"]


class RunDataRunID(Resource):
    def get(self, run_id):
        app.logger.debug("Requesting data for run with run number %s"
                         % run_id)
        result = mongo.db.runs_new.find_one_or_404({"number": run_id})
        return result["data"]


class RunDataTimestamp(Resource):
    def get(self, timestamp):
        app.logger.debug("Requesting data for run with timestamp %s"
                         % timestamp)
        result = mongo.db.runs_new.find_one_or_404({"name": timestamp})
        return result["data"]


api.add_resource(RunDataObjectID, '/run/objectid/<ObjectId:object_id>/tags')
api.add_resource(RunDataRunID, '/run/runnumber/<int:run_id>/tags')
api.add_resource(RunDataTimestamp, '/run/timestamp/<string:timestamp>/tags')
