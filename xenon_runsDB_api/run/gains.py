import flask
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo, config
from xenon_runsDB_api.common.util import result_formatting

"""
Getting and editing the gains for a run
"""

# webargs/Marshmellow de/serialization object definition
# In this case the gain object is a list of floats, that are greater than or 
# equal to 0. 
gain_args = {"gains": 
             fields.List(fields.Float(validate=lambda val: val >= 0.),
                                      required=True)}


class Gains(Resource):
    """
    Super class that provides semi-hidden generalized versions of functions
    needed to GET and PUT for the gains. 
    """

    def __init__(self):
        self.mongodb = mongo.db[config["runsDB"]["database_name"]]
        self.views = {config["runsDB"]["views"]["gains"]: 1}.update(
            config["runsDB"]["views"]["limited_view"])

    def _get_(self, key, value):
        """
        Generalized GET function to retrieve the gains

        Args:
            key (string): Key to limit query by
            value (string, int, BSON object ID): Search limit value

        Returns:
            If query successful: JSON object with run identifiers and the gains
            If not: returns 404
        """
        result = self.mongodb.find_one_or_404({key: value}, self.views)
        app.logger.debug("Query gains: %s "
                         % result)
        return flask.jsonify({"results": result}) 

    def _put_(self, key, value, gains):
        """
        Generalized PUT function to insert gains

        Args:
            key (string): Key to limit query by
            value (string, int, BSON object ID): Search limit value
            gains (list of floats): Gains to use in this DB object

        Returns:
            JSON object that shows the run document before and after the change
        """

        run_doc_before = mongodb.find_one_or_404({key: value}, self.views)
        run_doc_before = result_formatting(run_doc_before, "processor",
            "DEFAULT", "gains")
        self.mongodb.find_one_and_update({key: value},
            {"$set": {config["runsDB"]["views"]["gains"]: gains}})
        run_doc_after = mongodb.find_one_or_404({key: value}, self.views)
        run_doc_after = result_formatting(run_doc_after, "processor",
            "DEFAULT", "gains")
        return flask.jsonify({"previous_run_doc": run_doc_before,
                              "new_run_doc": run_doc_after})


class RunObjectIDGains(Gains):
    """
    Inherited class from run that provides interface when using object IDs
    """
    def get(self, object_id):
        return self._get_("_id", object_id)

    # Decorater passes the "gains" object that was parsed out of the json
    # piece of the PUT request to the kwarg of the function
    @use_kwargs(gain_args, locations=["json"])
    def put(self, object_id, gains):
        return self._put_("_id", object_id, gains)


class RunRunIDGains(Gains):
    """
    Inherited class from run that provides interface when using run number
    """
    def get(self, run_number):
        return self._get_("number", run_number)

    # Decorater passes the "gains" object that was parsed out of the json
    # piece of the PUT request to the kwarg of the function
    @use_kwargs(gain_args, locations=["json"])
    def put(self, run_number, gains):
        return self._put_("number", run_number, gains)


class RunTimestampGains(Gains):
    """
    Inherited class from run that provides interface when using timestamp
    """
    def get(self, timestamp):
        return self._get_("timestamp", timestamp)

    # Decorater passes the "gains" object that was parsed out of the json
    # piece of the PUT request to the kwarg of the function
    @use_kwargs(gain_args, locations=["json"])
    def put(self, timestamp, gains):
        return self._put_("name", timestamp, gains)


# Adding routes according what identifier is used.
api.add_resource(RunObjectIDGains,
                 '/run/objectid/<ObjectId:object_id>/gains/',
                 endpoint="run_object_id_gains")
api.add_resource(RunRunIDGains,
                 '/run/runnumber/<int:run_number>/gains/',
                 endpoint="run_run_id_gains")
api.add_resource(RunRunIDGains,
                 '/run/number/<int:run_number>/gains/',
                 endpoint="run_run_number_gains")
api.add_resource(RunTimestampGains,
                 '/run/timestamp/<string:timestamp>/gains/',
                 endpoint="run_timestamp_gains")
api.add_resource(RunTimestampGains,
                 '/run/name/<string:timestamp>/gains/',
                 endpoint="run_timestamp_name_gains")
# Including the path for runs. Just in case we change our
# mind down the road
api.add_resource(RunObjectIDGains,
                 '/runs/objectid/<ObjectId:object_id>/gains/',
                 endpoint="runs_object_id_gains")
api.add_resource(RunRunIDGains,
                 '/runs/runnumber/<int:run_number>/gains/',
                 endpoint="runs_run_id_gains")
api.add_resource(RunRunIDGains,
                 '/runs/number/<int:run_number>/gains/',
                 endpoint="runs_run_number_gains")
api.add_resource(RunTimestampGains,
                 '/runs/timestamp/<string:timestamp>/gains/',
                 endpoint="runs_timestamp_gains")
api.add_resource(RunTimestampGains,
                 '/runs/name/<string:timestamp>/gains/',
                 endpoint="runs_timestamp_name_gains")