from flask_restful import Resource
import ast
from flask import request
from marshmallow import Schema
from webargs import fields
from webargs.flaskparser import use_args
from xenon_runsDB_api.app import app, api, mongo


class runschema(Schema):
    name = fields.Str()
    number = fields.Int()
    detector = fields.Str()

user_args = {
    'where': fields.Dict(keys=fields.Str())
}

class RunsQuery(Resource):
    def __init__(self):
        self.valid_query_requests = ["query", "q"]

    # def reduce_args(self, args):
    #     query = None
    #     for k, v in args.items():
    #         if k not in self.valid_query_requests:
    #             continue
    #         query = ast.literal_eval(v)
    #     return query




    @use_args(user_args)
    def get(self):
        # args = request.args
        app.logger.debug("args passed to query: %s"
                         % args)
        app.logger.debug("%s" % request.form["data"])
        query = self.reduce_args(args)
        cursor = mongo.db.runs_new.find(query)
        results = [x for x in cursor]
        if len(results) == 1:
            return results[0]
        else:
            return results


api.add_resource(RunsQuery,
                 '/run/query',
                 endpoint="run_query")
api.add_resource(RunsQuery,
                 '/runs/query',
                 endpoint="runs_query")
