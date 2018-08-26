from flask_restful import Resource
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api

class RunsTag(Resource):
    def get(self, tag):
        app.logger.debug("Getting all runs with tag %s" % tag)
        results = util.get_data_single_top_level(query, "data")
        return results


api.add_resource(RunsTag, '/runs/tag/<string:tag>/')
