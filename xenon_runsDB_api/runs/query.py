from flask_restful import Resource
import ast
from flask import request
from xenon_runsDB_api.app import api, mongo


class RunsQuery(Resource):
    def __init__(self):
        self.valid_query_requests = ["query", "q"]

    # @use_args(user_args)
    def get(self):
        args = request.args
        for k, v in args.items():
            if k not in self.valid_query_requests:
                continue
            query = ast.literal_eval(v)
        cursor = mongo.db.runs_new.find(query)
        results = [x for x in cursor]
        if len(results) == 1:
            return results[0]
        else:
            return results


api.add_resource(RunsQuery, '/run/query')
api.add_resource(RunsQuery, '/runs/query')
