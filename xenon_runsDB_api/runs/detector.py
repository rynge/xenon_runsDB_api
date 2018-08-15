from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo


class RunsDetector(Resource):
    def get(self, detector, data_field=None):
        app.logger.debug('Requesting all runs with detector: %s',
                         detector)
        query = {{'detector': detector}}
        results = util.get_data_single_top_level(query, data_field)
        app.logger.debug('Requesting %s records',
                         cursor.count())
        return results


api.add_resource(RunsDetector, '/runs/detector/<string:detector>/')
