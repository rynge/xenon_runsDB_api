import flask
import flask_praetorian
from flask_restful import Resource
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api, mongo


class RunsProcessingVersion(Resource):
    @flask_praetorian.roles_required('user')
    def get(self, version):
        app.logger.debug('Requesting all runs with status: %s', status)
        if not version.startswith('v'):
            version = "v" + version
        query = {"data": {"$elemMatch": {"type": "processed",
                                         "status": "transferred",
                                         "pax_version": version}}}
        results = util.get_data_single_top_level(query, "data")
        app.logger.debug("results: %s" % results)
        if results:
            return results
        else:
            return flask.abort(404)


api.add_resource(RunsProcessingVersion, 
                 '/runs/process_version/<string:version>')