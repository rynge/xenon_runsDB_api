import flask
from flask_restful import Resource
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api


class RunsLocationList(Resource):
    def get(self, location, data_field=None):
        query = {"data": {"$elemMatch": {"host": "rucio-catalogue",
                                         "rse": location}}}
        results = util.get_data_single_top_level(query)
        if results:
            return flask.jsonify({"results": results})
        else:
            return flask.abort(404,
                               "No run with location {} found".format(location))


api.add_resource(RunsLocationList,
                 '/runs/location/<string:location>/',
                 '/runs/location/<string:location>/<string:data_field>')
