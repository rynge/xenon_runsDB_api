from flask_restful import Resource
from xenon_runsDB_api import util
from xenon_runsDB_api.app import app, api, mongo


class RunStatusObjectID(Resource):
    def put(self, object_id, status):
        app.logger.debug("Requesting data for run with object ID %s"
                    % object_id)
        result = mongo.db["runs_new"].find_one_or_404(
            {"_id": object_id})
        # change result according
        if status == "not_processed":
            query = {"$not": {"$elemMatch": {"type": "processed"}},
                     "$elemMatch": {"type": "raw",
                                    "status": "transferred"}}
        elif status == "processing":
            query = {"$elemMatch": {"type": "processed",
                                    "status": "processing"}}
        elif status == "processed":
            # No processed data and raw data is transferring
            query = {"$elemMatch": {"type": "processed",
                                    "status": "processed"}}
        elif status == "transferring":
            # No processed data and raw data is transferring
            query = {"$not": {"$elemMatch": {"type": "processed"}},
                     "$elemMatch": {"type": "raw",
                                    "status": "transferring"}}


class RunStatusRunNumber(Resource):
    def put(self, run_number, status):
        app.logger.debug("Requesting data for run with run number %s"
                         % run_number)
        result = mongo.db["runs_new"].find_one_or_404(
            {"number": run_number})



class RunStatusTimestamp(Resource):
    def put(self, timestamp, status):
        app.logger.debug("Requesting data for run with timestamp %s",
                    timestamp)
        result = mongo.db["runs_new"].find_one_or_404(
            {"name": timestamp})
        


# Adding routes according what identifier is used.
api.add_resource(RunObjectID,
                 '/run/objectid/<ObjectId:object_id>/<string:status>',
                 endpoint="run_object_id_status")
api.add_resource(RunRunNumber,
                 '/run/runnumber/<int:run_number>/<string:status>',
                 endpoint="run_run_id_status")
api.add_resource(RunRunNumber,
                 '/run/number/<int:run_number>/<string:status>',
                 endpoint="run_run_number_status")
api.add_resource(RunTimestamp,
                 '/run/timestamp/<string:timestamp>/<string:status>',
                 endpoint="run_timestamp_status")
api.add_resource(RunTimestamp,
                 '/runs/name/<string:timestamp>/<string:status>',
                 endpoint="run_timestamp_name_status")
# Including the path for runs. Just in case we change our
# mind down the road
api.add_resource(RunObjectID,
                 '/runs/objectid/<ObjectId:object_id>/<string:status>',
                 endpoint="runs_object_id_status")
api.add_resource(RunRunNumber,
                 '/runs/runnumber/<int:run_number>/<string:status>',
                 endpoint="runs_run_id_status")
api.add_resource(RunRunNumber,
                 '/runs/number/<int:run_number>/<string:status>',
                 endpoint="runs_run_number_status")
api.add_resource(RunTimestamp,
                 '/runs/timestamp/<string:timestamp>/<string:status>',
                 endpoint="runs_timestamp_status")
api.add_resource(RunTimestamp,
                 '/runs/name/<string:timestamp>/<string:status>',
                 endpoint="runs_timestamp_name_status")