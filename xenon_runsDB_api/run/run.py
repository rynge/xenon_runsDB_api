import flask
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo

"""
Deleting, getting, inserting, the entire document for 
a run given a unique identifier for the desired run. In this 
case there are three possible identifiers the database specific
documennt or object ID, the run number (or run id), 
and the timestamp in YYMMDD_HHMM format.
"""


class Run(Resource):
    """
    Super class that provides semi-hidden generalized versions of functions
    needed to GET and DELETE. Provides 

    TODO: Finish POST function for run documents. 
    """
    def _get_(self, key, value):
        """
        Generalized GET function to make DB retrieval calls

        Args:
            key (string): Key in the run document to filter by
            value (string, int, BSON object ID): Search limit value
        
        Returns:
            If query successful: JSON object of the run document
            If not: returns 404
        """
        app.logger.debug("Requesting data for run with %s %s"
                         % (key, value))
        result = mongo.db["runs_new"].find_one_or_404(
            {key: value})
        app.logger.debug("Keys for result: %s" % result.keys())
        return flask.jsonify({"results": result})
    
    def _delete_(self, key, value):
        """
        Generalized DELETE function to make DB delete calls

        Args:
            key (string): Key in the run document
            value (string, int, BSON object ID): Search limit

        Returns:
            Empty string and status 204
        """
        mongo.db["runs_new"].delete_one({key: value})
        return '', 204
    
    def post(self, doc):
        """
        TODO: Add webargs to parse the json doc needed.

        Function to add a run document

        Args:
            doc (JSON): Run document to be added
        """
        mongo.db["runs_new"].insert_one(doc)


class RunObjectID(Run):
    """
    Inherited class from run that provides interface when using object IDs
    """
    def get(self, object_id):
        return self._get_("_id", object_id)

    def delete(self, object_id):
        return self._delete_("_id", object_id)


class RunRunNumber(Run):
    """
    Inherited class from run that provides interface when using the run number
    """
    def get(self, run_number):
        return self._get_("number", run_number)

    def delete(self, run_number):
        return self._delete_("number", run_number)


class RunTimestamp(Run):
    """
    Inherited class from run that provides interface when using the run start
    timestamp
    """
    def get(self, timestamp):
        return self._get_("name", timestamp)

    def delete(self, timestamp):
        return self._delete_("name", timestamp)


# Adding routes according what identifier is used.
api.add_resource(RunObjectID,
                 '/run/objectid/<ObjectId:object_id>/',
                 endpoint="run_object_id")
api.add_resource(RunRunNumber,
                 '/run/runnumber/<int:run_number>/',
                 endpoint="run_run_number")
api.add_resource(RunRunNumber,
                 '/run/number/<int:run_number>/',
                 endpoint="run_number")
api.add_resource(RunTimestamp,
                 '/run/timestamp/<string:timestamp>/',
                 endpoint="run_timestamp")
api.add_resource(RunTimestamp,
                 '/runs/name/<string:timestamp>/',
                 endpoint="run_timestamp_name")
# Including the path for runs. Just in case we change our
# mind down the road
api.add_resource(RunObjectID,
                 '/runs/objectid/<ObjectId:object_id>/',
                 endpoint="runs_object_id")
api.add_resource(RunRunNumber,
                 '/runs/runnumber/<int:run_number>/',
                 endpoint="runs_run_id")
api.add_resource(RunRunNumber,
                 '/runs/number/<int:run_number>/',
                 endpoint="runs_run_number")
api.add_resource(RunTimestamp,
                 '/runs/timestamp/<string:timestamp>/',
                 endpoint="runs_timestamp")
api.add_resource(RunTimestamp,
                 '/runs/name/<string:timestamp>/',
                 endpoint="runs_timestamp_name")
# Path for insert new run doc with either /run/ or /runs
api.add_resource(Run,
                 "/run/insert",
                 "/runs/insert",
                 endpoint="run_insert")

