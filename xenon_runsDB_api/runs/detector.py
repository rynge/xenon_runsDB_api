import flask_praetorian
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo


class RunsDetector(Resource):
    @flask_praetorian.roles_required('user')
    def get(self, detector, data_field=None):
        app.logger.debug('Requesting all runs with detector: %s',
                         detector)
        query = {'detector': detector}
        results = util.get_data_single_top_level(query, data_field)
        if results:
            return flask.jsonify({"results": results})
        else:
            return flask.abort(404, "No run with tag {} found".format(tag))


api.add_resource(RunsDetector,
                 '/runs/detector/<string:detector>/',
                 '/runs/detector/<string:detector>/<string:data_field>')
