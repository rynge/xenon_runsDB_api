from flask_restful import Resource
from xenon_runsDB_api import app, api, mongo


class RunsTag(Resource):
    def get(self, tag):
        app.logger.debug("Getting all runs with tag %s" % tag)
        cursor = mongo.db.runs_new.find({"tags.name": tag})
        app.logger.debug('Total documents requested %s', cursor.count())
        results = [x for x in cursor]
        return results


api.add_resource(RunsTag, '/runs/tag/<string:tag>')
