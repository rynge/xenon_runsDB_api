import flask
import flask_praetorian
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from xenon_runsDB_api.app import app, api, mongo, config


user_args = {
    'query': fields.Dict()
}

class RunsQuery(Resource):

    def __init__(self):
        self.mongodb = mongo.db[config["runsDB"]["database_name"]]

    @use_args(user_args)
    def post(self, args, locations=["json"]):
        # args = request.args
        app.logger.debug("args passed to query: %s"
                         % args)
        query = args["query"]
        cursor = self.mongodb.find(query)
        results = [x for x in cursor]
        app.logger.debug("results: %s" % results)
        return flask.jsonify({"results": results})


api.add_resource(RunsQuery,
                 '/runs/query',
                 endpoint="runs_query")
