import flask
from flask_restful import Resource
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api, mongo


class RunsSource(Resource):
    def get(self, source, data_field=None):
        app.logger.debug('Requesting all runs with source: %s', source)
        if source == "calibration":
            query = {"source.type": {"$not": {"$eq": "none"}}}
        else:
            query = {"source.type": source}
        app.logger.debug("query: {}".format(query))
        results = util.get_data_single_top_level(query, data_field)
        app.logger.debug("results: %s" % results)
        if results:
            return flask.jsonify({"results": results})
        else:
            return flask.abort(404, 
                               "No run with source {} found".format(source))

api.add_resource(RunsSource,
                 '/runs/source/<string:source>/',
                 '/runs/source/<string:source>/<string:data_field>/')