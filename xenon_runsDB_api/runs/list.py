import flask
from flask_restful import Resource
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api, mongo


class RunsList(Resource):
    def get(self, data_field=None):
        app.logger.debug("Getting ALL runs")
        results = util.get_data_single_top_level({}, data_field)
        if results:
            return flask.jsonify({"results": results})
        else:
            return flask.abort(404, 
                               "No runs found. Check the database!")


api.add_resource(RunsList,
                 '/runs/',
                 '/runs/<string:data_field>')
