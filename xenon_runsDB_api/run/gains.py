from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo


def get_result_ready(result):
        return result["processor"]["DEFAULT"]["gains"]


class RunGainsObjectID(Resource):
    def get(self, object_id):
        app.logger.debug("Requesting data for run with object ID %s"
                         % object_id)
        result = mongo.db.runs_new.find_one_or_404({"_id": object_id})
        return get_result_ready(result)


class RunGainsRunID(Resource):
    def get(self, run_id):
        app.logger.debug("Requesting data for run with run number %s"
                         % run_id)
        result = mongo.db.runs_new.find_one_or_404({"number": run_id})
        return get_result_ready(result)


class RunGainsTimestamp(Resource):
    def get(self, timestamp):
        app.logger.debug("Requesting data for run with timestamp %s"
                         % timestamp)
        result = mongo.db.runs_new.find_one_or_404({"name": timestamp})
        return get_result_ready(result)


api.add_resource(RunGainsObjectID,
                 ('/run/objectid/<ObjectId:object_id>/'
                  'processor/DEFAULT/gains/'))
api.add_resource(RunGainsRunID,
                 ('/run/runnumber/<int:run_id>/'
                  'processor/DEFAULT/gains/'))
api.add_resource(RunGainsTimestamp,
                 ('/run/timestamp/<string:timestamp>/'
                  'processor/DEFAULT/gains/'))
