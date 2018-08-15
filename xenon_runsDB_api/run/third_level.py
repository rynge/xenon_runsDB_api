from flask import abort
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo

"""
Getting the entire document for a run given a unique identifier for
the desired run. In this case there are three possible identifiers
the database specific documennt or object ID, the run number
(or run id), and the timestamp in YYMMDD_HHMM format.
"""

class RunThirdLevelObjectID(Resource):
    def get(self, object_id, top_level, second_level, third_level):
        app.logger.debug("Requesting data for run with object ID %s"
                         % object_id)
        result = mongo.db.runs_new.find_one_or_404(
            {"_id": object_id},
            {"_id": 0,
             "%s.%s.%s" % (top_level, second_level, third_level): 1})
        app.logger.debug("Query Result %s" % result)
        if not result:
            return abort(404)
        else:
            return result[top_level][second_level][third_level]


class RunThirdLevelRunID(Resource):
    def get(self, run_id, top_level, second_level, third_level):
        app.logger.debug("Requesting data for run with run number %s"
                         % run_id)
        result = mongo.db.runs_new.find_one_or_404(
            {"number": run_id},
            {"_id": 0,
             "%s.%s.%s" % (top_level, second_level, third_level): 1})
        if not result:
            return abort(404)
        else:
            return result[top_level][second_level][third_level]


class RunThirdLevelTimestamp(Resource):
    def get(self, timestamp, top_level, second_level, third_level):
        app.logger.debug("Requesting data for run with timestamp %s"
                         % timestamp)
        result = mongo.db.runs_new.find_one_or_404(
            {"name": timestamp},
            {"_id": 0,
             "%s.%s.%s" % (top_level, second_level, third_level): 1})
        if not result:
            return abort(404)
        else:
            return result[top_level][second_level][third_level]


api.add_resource(RunThirdLevelObjectID,
                 ('/run/objectid/<ObjectId:object_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="run_object_id_thirdlevel")
api.add_resource(RunThirdLevelRunID,
                 ('/run/runnumber/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="run_run_id_thirdlevel")
api.add_resource(RunThirdLevelTimestamp,
                 ('/run/timestamp/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="run_timestamp_thirdlevel")

api.add_resource(RunThirdLevelObjectID,
                 ('/runs/objectid/<ObjectId:object_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="runs_object_id_thirdlevel")
api.add_resource(RunThirdLevelRunID,
                 ('/runs/runnumber/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="runs_run_id_thirdlevel")
api.add_resource(RunThirdLevelTimestamp,
                 ('/runs/timestamp/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="runs_timestamp_thirdlevel")
