from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo
# from bson.json_util import dumps


class RunObjectID(Resource):
    def get(self, object_id):
        app.logger.debug("Requesting data for run with object ID %s"
                         % object_id)
        return mongo.db.runs_new.find_one_or_404({"_id": object_id})

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
        return mongo.db.runs_new.find_one_or_404({"number": run_id})

    def delete(self, run_id):
        mongo.db.runs_new.find_one_or_404({"number": run_id})
        mongo.db.runs_new.remove({"number": run_id})
        return '', 204


class RunTimestamp(Resource):
    def get(self, timestamp):
        app.logger.debug("Requesting data for run with timestamp %s"
                         % timestamp)
        return mongo.db.runs_new.find_one_or_404({"name": timestamp})

    def delete(self, timestamp):
        mongo.db.runs_new.find_one_or_404({"name": timestamp})
        mongo.db.runs_new.remove({"name": timestamp})
        return '', 204


api.add_resource(RunObjectID, '/run/objectid/<ObjectId:object_id>')
api.add_resource(RunRunID, '/run/runnumber/<int:run_id>')
api.add_resource(RunTimestamp, '/run/timestamp/<string:timestamp>')
