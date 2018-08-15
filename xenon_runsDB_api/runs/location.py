from flask_restful import Resource
from xenon_runsDB_api import util
from xenon_runsDB_api.app import app, api


class RunsLocationList(Resource):
    def get(self, location):
        query = {"data": {"$elemMatch": {"host": "rucio-catalogue",
                                         "rse": location}}}
        return util.get_data_single_top_level(query)


class RunsLocationListDataType(Resource):
    def get(self, rse, data_field=None):
        query = {"data": {"$elemMatch": {"type": data_type,
                                         "rse": rse}}}
        return util.get_data_single_top_level(query, data_field)


api.add_resource(RunsLocationList,
                 '/runs/location/<string:location>/')
api.add_resource(RunsLocationListDataType,
                 '/runs/location/<string:location>/<string:data_type>')
