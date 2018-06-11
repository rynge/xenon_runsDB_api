from flask_restful import Resource
from xenon_runsDB_api import app, api, mongo


class RunsSubdetector(Resource):
    def get(self, subdetector):
        app.logger.debug('Requesting all runs with subdetector: %s',
                         subdetector)
        # app.logger.debug('%s', mongo.db.runs_new.find({'status': status}))
        return [x for x in mongo.db.runs_new.find({'status': subdetector})]


api.add_resource(RunsSubdetector, '/runs/subdectector/<string:subdetector>')
