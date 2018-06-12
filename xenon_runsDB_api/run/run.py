from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo


class RunObjectID(Resource):
    def get(self, object_id):
        app.logger.debug("Requesting data for run with object ID %s"
                         % object_id)
        result = mongo.db.runs_new.find_one_or_404({"_id": object_id})
        app.logger.debug("Keys for result: %s" % result.keys())
        return result

    def delete(self, object_id):
        app.logger.debug("Deleting data for run with object ID %s"
                         % object_id)
        mongo.db.runs_new.find_one_or_404({"_id": object_id})
        mongo.db.runs_new.remove({"_id": object_id})
        return '', 204


class RunRunID(Resource):
    def get(self, run_id):
        app.logger.debug("Requesting data for run with run number %s"
                         % run_id)
        result = mongo.db.runs_new.find_one_or_404({"number": run_id})
        app.logger.debug("Keys for result: %s" % result.keys())
        return result

    def delete(self, run_id):
        mongo.db.runs_new.find_one_or_404({"number": run_id})
        mongo.db.runs_new.remove({"number": run_id})
        return '', 204


class RunTimestamp(Resource):
    def get(self, timestamp):
        app.logger.debug("Requesting data for run with timestamp %s"
                         % timestamp)
        result = mongo.db.runs_new.find_one_or_404({"name": timestamp})
        app.logger.debug("Keys for result: %s" % result.keys())
        return result

    def delete(self, timestamp):
        mongo.db.runs_new.find_one_or_404({"name": timestamp})
        mongo.db.runs_new.remove({"name": timestamp})
        return '', 204


api.add_resource(RunObjectID,
                 '/run/objectid/<ObjectId:object_id>/',
                 endpoint="run_object_id")
api.add_resource(RunRunID,
                 '/run/runnumber/<int:run_id>/',
                 endpoint="run_run_id")
api.add_resource(RunTimestamp,
                 '/run/timestamp/<string:timestamp>/',
                 endpoint="run_timestamp")

api.add_resource(RunObjectID,
                 '/runs/objectid/<ObjectId:object_id>/',
                 endpoint="runs_object_id")
api.add_resource(RunRunID,
                 '/runs/runnumber/<int:run_id>/',
                 endpoint="runs_run_id")
api.add_resource(RunTimestamp,
                 '/runs/timestamp/<string:timestamp>/',
                 endpoint="runs_timestamp")
