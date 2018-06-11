from flask_restful import Resource
from xenon_runsDB_api import app, api, mongo


class RunsStatus(Resource):
    def get(self, status):
        app.logger.debug('Requesting all runs with status: %s', status)
        cursor = mongo.db.runs_new.find({'status.%s' % status: True})
        app.logger.debug('Requesting %s records' % cursor.count())
        return [x for x in cursor]


api.add_resource(RunsStatus, '/runs/status/<str:status>')
