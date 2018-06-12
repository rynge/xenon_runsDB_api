from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo


class RunThirdLevelObjectID(Resource):
    def get(self, object_id, top_level, second_level, third_level):
        app.logger.debug("Requesting data for run with object ID %s"
                         % object_id)
        result = mongo.db.runs_new.find_one_or_404({"_id": object_id})
        return 404
        # if (isinstance(result[top_level], list) or
        #     isinstance(result[top_level], tuple)):
        #     filtered_results = [record[second_level]
        #                         for record in result[top_level]]
        #     return filtered_results
        # if isinstance(result[top_level], dict):
        #     return result[top_level][second_level]
        # if not (isinstance(result[top_level], list) or
        #         isinstance(result[top_level], tuple) or
        #         isinstance(result[top_level], dict)):
        #     return 404


class RunThirdLevelRunID(Resource):
    def get(self, run_id, top_level, second_level, third_level):
        app.logger.debug("Requesting data for run with run number %s"
                         % run_id)
        result = mongo.db.runs_new.find_one_or_404({"number": run_id})
        return 404
        # if (isinstance(result[top_level], list) or
        #     isinstance(result[top_level], tuple)):
        #     filtered_results = [record[second_level]
        #                         for record in result[top_level]]
        #     return filtered_results
        # if isinstance(result[top_level], dict):
        #     return result[top_level][second_level]
        # if not (isinstance(result[top_level], list) or
        #         isinstance(result[top_level], tuple) or
        #         isinstance(result[top_level], dict)):
        #     return 404


class RunThirdLevelTimestamp(Resource):
    def get(self, timestamp, top_level, second_level, third_level):
        app.logger.debug("Requesting data for run with timestamp %s"
                         % timestamp)
        result = mongo.db.runs_new.find_one_or_404({"name": timestamp})
        return 404
        # if (isinstance(result[top_level], list) or
        #     isinstance(result[top_level], tuple)):
        #     filtered_results = [record[second_level]
        #                         for record in result[top_level]]
        #     return filtered_results
        # if isinstance(result[top_level], dict):
        #     return result[top_level][second_level]
        # if not (isinstance(result[top_level], list) or
        #         isinstance(result[top_level], tuple) or
        #         isinstance(result[top_level], dict)):
        #     return 404


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
