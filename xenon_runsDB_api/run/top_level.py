import flask
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo

"""
Getting the top-level entry in the document for a run given a 
unique identifier for the desired run. In this case there are three possible 
identifiers the database specific document or object ID, the run number
(or run id), and the timestamp in YYMMDD_HHMM format.
"""

class RunTopLevel(Resource):
    """
    Super class that provides semi-hidden generalized versions of functions
    needed to GET.
    
    TODO: Create PUT - Update first level doc 
    """
    def _get_(self, key, value, top_level):
        """
        Generalized GET function to make DB retrieval calls and limits return
        to desired information.

        Args:
            key (string): Key in the run document to filter by
            value (string, int, BSON object ID): Search limit value
            top_level (string): Top level key in run document to return to user
        
        Returns:
            If query successful: JSON object with limited run document
            If not: returns 404
        """
        result = mongo.db.runs_new.find_one_or_404(
            {key: value},
            {"_id": 1,
             "name": 1,
             "number": 1,
             top_level: 1})
        app.logger.debug("Query result: %s "
                         % result)
        return flask.jsonify({"results": result})
        

class RunTopLevelObjectID(RunTopLevel):
    """
    Inherited class from run that provides interface when using object IDs
    """
    def get(self, object_id, top_level):
        app.logger.debug(("Requesting {top_level} data for run "
                          "with object ID {object_id}").format(
                              top_level=top_level,
                              object_id=object_id))
        return self._get_("_id", object_id, top_level)


class RunTopLevelRunID(RunTopLevel):
    """
    Inherited class from run that provides interface when using the run number
    """
    def get(self, run_id, top_level):
        app.logger.debug(("Requesting {top_level} data for run "
                          "with run number {run_id}").format(
                              top_level=top_level,
                              run_id=run_id))
        return self._get_("number", run_id, top_level)


class RunTopLevelTimestamp(RunTopLevel):
    """
    Inherited class from run that provides interface when using the run start
    timestamp
    """
    def get(self, timestamp, top_level):
        app.logger.debug(("Requesting {top_level} data for run "
                          "with name {timestamp}").format(
                              top_level=top_level,
                              timestamp=timestamp))
        return self._get_("name", timestamp, top_level)


# Defining the routes and what they mean
api.add_resource(RunTopLevelObjectID,
                 '/run/objectid/<ObjectId:object_id>/<string:top_level>/',
                 endpoint="run_object_id_toplevel")
api.add_resource(RunTopLevelRunID,
                 '/run/runnumber/<int:run_id>/<string:top_level>/',
                 endpoint="run_run_id_toplevel")
api.add_resource(RunTopLevelRunID,
                 '/run/number/<int:run_id>/<string:top_level>/',
                 endpoint="run_number_toplevel")
api.add_resource(RunTopLevelTimestamp,
                 '/run/timestamp/<string:timestamp>/<string:top_level>/',
                 endpoint="run_timestamp_toplevel")
api.add_resource(RunTopLevelTimestamp,
                 '/run/name/<string:timestamp>/<string:top_level>/',
                 endpoint="run_name_toplevel")

api.add_resource(RunTopLevelObjectID,
                 '/runs/objectid/<ObjectId:object_id>/<string:top_level>/',
                 endpoint="runs_object_id_toplevel")
api.add_resource(RunTopLevelRunID,
                 '/runs/runnumber/<int:run_id>/<string:top_level>/',
                 endpoint="runs_run_id_toplevel")
api.add_resource(RunTopLevelRunID,
                 '/runs/number/<int:run_id>/<string:top_level>/',
                 endpoint="runs_run_number_toplevel")             
api.add_resource(RunTopLevelTimestamp,
                 '/runs/timestamp/<string:timestamp>/<string:top_level>/',
                 endpoint="runs_timestamp_toplevel")
api.add_resource(RunTopLevelTimestamp,
                 '/runs/name/<string:timestamp>/<string:top_level>/',
                 endpoint="runs_name_toplevel")
