from flask_restful import Resource
from xenon_runsDB_api import app, api, mongo


class RunsList(Resource):
    def get(self):
        app.logger.debug("Getting ALL runs")
        cursor = mongo.db.runs_new.find()
        app.logger.debug('Total documents requested %s', cursor.count())
        results = [x for x in cursor]
        return results


api.add_resource(RunsList, '/runs')
