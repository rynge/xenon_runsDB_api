from flask_restful import Resource
from xenon_runsDB_api import util
from xenon_runsDB_api.app import app, api, mongo


class RunsSource(Resource):
    def get(self, source, data_field=None):
        app.logger.debug('Requesting all runs with status: %s', status)
        query = {"source.type": source}
        results = util.get_data_single_top_level(query, data_field)
        app.logger.debug("results: %s" % results)
        if results:
            return results
        else:
            return abort(404)

api.add_resource(RunsSource,
                '/runs/source/<string:source>/<string:data_field>')