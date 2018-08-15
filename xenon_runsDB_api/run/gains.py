import flask
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo


gain_args = {"gains": 
            fields.List(fields.Float(validate=lambda val: val >= 0.),
                                     required=True)}


class Gains(Resource):
    def _put_(self, key, value, gains):
        run_doc_before = mongo.db["runs_new"].find_one_or_404(
            {key: value})
        mongo.db["runs_new"].find_one_and_update(
            {key: value},
            {"$set": {"processor.DEFAULT.gains": gains}}
        )
        run_doc_after = mongo.db["runs_new"].find_one_or_404(
            {key: value})
        return flask.jsonify({"previous_run_doc": run_doc_before,
                              "new_run_doc": run_doc_after})


class RunObjectIDGains(Gains):
    @use_kwargs(gain_args, locations=["json"])
    def put(self, object_id, gains):
        return self._put_("_id", object_id, gains)


class RunRunIDGains(Gains):
    @use_kwargs(gain_args, locations=["json"])
    def put(self, run_number, gains):
        return self._put_("number", run_number, gains)


class RunTimestampGains(Gains):
    @use_kwargs(gain_args, locations=["json"])
    def put(self, timestamp, gains):
        return self._put_("name", timestamp, gains)


# Adding routes according what identifier is used.
api.add_resource(RunObjectIDGains,
                 '/run/objectid/<ObjectId:object_id>/gains',
                 endpoint="run_object_id_gains")
api.add_resource(RunRunIDGains,
                 '/run/runnumber/<int:run_number>/gains',
                 endpoint="run_run_id_gains")
api.add_resource(RunRunIDGains,
                 '/run/number/<int:run_number>/gains',
                 endpoint="run_run_number_gains")
api.add_resource(RunTimestampGains,
                 '/run/timestamp/<string:timestamp>/gains',
                 endpoint="run_timestamp_gains")
api.add_resource(RunTimestampGains,
                 '/run/name/<string:timestamp>/gains',
                 endpoint="run_timestamp_name_gains")
# Including the path for runs. Just in case we change our
# mind down the road
api.add_resource(RunObjectIDGains,
                 '/runs/objectid/<ObjectId:object_id>/gains',
                 endpoint="runs_object_id_gains")
api.add_resource(RunRunIDGains,
                 '/runs/runnumber/<int:run_number>/gains',
                 endpoint="runs_run_id_gains")
api.add_resource(RunRunIDGains,
                 '/runs/number/<int:run_number>/gains',
                 endpoint="runs_run_number_gains")
api.add_resource(RunTimestampGains,
                 '/runs/timestamp/<string:timestamp>/gains',
                 endpoint="runs_timestamp_gains")
api.add_resource(RunTimestampGains,
                 '/runs/name/<string:timestamp>/gains',
                 endpoint="runs_timestamp_name_gains")