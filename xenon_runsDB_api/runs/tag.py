import flask
import flask_praetorian
from flask_restful import Resource
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api

class RunsTag(Resource):
    @flask_praetorian.roles_required('user')
    def get(self, tag, data_field=None):
        app.logger.debug("Getting all runs with tag %s" % tag)
        query = {"tags.name": tag}
        results = util.get_data_single_top_level(query, data_field)
        if results:
            return flask.jsonify({"results": results})
        else:
            return flask.abort(404, "No run with tag {} found".format(tag))


api.add_resource(RunsTag,
                 '/runs/tag/<string:tag>/',
                 '/runs/tag/<string:tag>/<string:data_field>'
                 )
