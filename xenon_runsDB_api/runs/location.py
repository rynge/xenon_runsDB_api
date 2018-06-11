from flask_restful import Resource
from xenon_runsDB_api import app, api, mongo
from bson.json_util import dumps


class RunsList(Resource):
    def get(self):
        for x in mongo.db.runs_new.find():
            json_dump = dumps(x)
            app.logger.debug('%s', json_dump)
            app.logger.debug('%s', x.keys())
        return [x for x in mongo.db.runs_new.find()]


api.add_resource(RunsList, '/runs/')
