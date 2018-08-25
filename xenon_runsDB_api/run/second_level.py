import inspect
import flask
from flask_restful import Resource
from xenon_runsDB_api.common.util import get_result_ready
from xenon_runsDB_api.app import app, api, mongo

"""
Getting the second-level entry document for a run given a unique identifier for
the desired run. In this case there are three possible identifiers
the database specific document or object ID, the run number
(or run id), and the timestamp in YYMMDD_HHMM format.
"""

class RunSecondLevel(Resource):
    """
    Super class that provides semi-hidden generalized versions of functions
    needed to GET.

    TODO: Create PUT - Update second level doc 
    """
    def _get_(self, key, value, top_level, second_level):
        """
        Generalized GET function to make DB retrieval calls and limits return
        to desired information.

        Args:
            key (string): Key in the run document to filter by
            value (string, int, BSON object ID): Search limit value
            top_level (string): Top level key in run document to return to user
            second_level (string): Key to the first nested quantity in the 
                                   top level object
        
        Returns:
            If query successful: JSON object with limited run document
            If not: returns 404
        """
        result = mongo.db.runs_new.find_one_or_404(
            {key: value},
            {"_id": 1,
             "name": 1,
             "number": 1,
             "{first}.{second}".format(first=top_level, 
                                       second=second_level): 1})
        app.logger.debug("Query result: %s "
                         % result)
        return flask.jsonify({"results": result})


class RunSecondLevelObjectID(RunSecondLevel):
    """
    Inherited class from run that provides interface when using object IDs
    """
    def get(self, object_id, top_level, second_level):
        app.logger.debug(("Requesting {top_level}.{second_level} data for run "
                          "with object ID {object_id}").format(
                              top_level=top_level,
                              second_level=second_level,
                              object_id=object_id))
        return self._get_("_id", object_id, top_level, second_level)


class RunSecondLevelRunID(RunSecondLevel):
    """
    Inherited class from run that provides interface when using the run number
    """
    def get(self, run_id, top_level, second_level):
        app.logger.debug(("Requesting {top_level}.{second_level} data for run "
                          "with run number {run_id}").format(
                              top_level=top_level,
                              second_level=second_level,
                              run_id=run_id))
        return self._get_("number", run_id, top_level, second_level)


class RunSecondLevelTimestamp(RunSecondLevel):
    """
    Inherited class from run that provides interface when using the run start
    timestamp
    """
    def get(self, timestamp, top_level, second_level):
        app.logger.debug(("Requesting {top_level}.{second_level} data for run "
                          "with run name {timestamp}").format(
                              top_level=top_level,
                              second_level=second_level,
                              timestamp=timestamp))
        return self._get_("name", timestamp, top_level, second_level) 


api.add_resource(RunSecondLevelObjectID,
                 ('/run/objectid/<ObjectId:object_id>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="run_object_id_secondlevel")
api.add_resource(RunSecondLevelRunID,
                 ('/run/runnumber/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="run_run_id_secondlevel")
api.add_resource(RunSecondLevelRunID,
                 ('/run/number/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="run_number_secondlevel")
api.add_resource(RunSecondLevelTimestamp,
                 ('/run/timestamp/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="run_timestamp_secondlevel")
api.add_resource(RunSecondLevelTimestamp,
                 ('/run/name/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="run_name_secondlevel")

api.add_resource(RunSecondLevelObjectID,
                 ('/runs/objectid/<ObjectId:object_id>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="runs_object_id_secondlevel")
api.add_resource(RunSecondLevelRunID,
                 ('/runs/runnumber/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="runs_run_id_secondlevel")
api.add_resource(RunSecondLevelRunID,
                 ('/runs/number/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="runs_numbersecondlevel")
api.add_resource(RunSecondLevelTimestamp,
                 ('/runs/timestamp/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="runs_timestamp_secondlevel")
api.add_resource(RunSecondLevelTimestamp,
                 ('/runs/name/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'),
                 endpoint="runs_name_secondlevel")