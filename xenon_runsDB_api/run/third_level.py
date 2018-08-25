import flask
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, mongo

"""
Getting the third-level entry for run given a unique identifier for
the desired run. In this case there are three possible identifiers
the database specific documennt or object ID, the run number
(or run id), and the timestamp in YYMMDD_HHMM format.
"""

class RunThirdLevel(Resource):
    """
    Super class that provides semi-hidden generalized versions of functions
    needed to GET.

    TODO: Create PUT - Update third level doc 
    """
    def _get_(self, key, value, top_level, second_level, third_level):
        """
        Generalized GET function to make DB retrieval calls and limits return
        to desired information.

        Args:
            key (string): Key in the run document to filter by
            value (string, int, BSON object ID): Search limit value
            top_level (string): Top level key in run document to return to user
            second_level (string): Key to the first nested quantity in the 
                                   top level object
            third_level (string): Key of the first nested quantity in the
                                  second level object, i.e. second nested
                                  quantity of the top level objected
        
        Returns:
            If query successful: JSON object with limited run document
            If not: returns 404
        """
        result = mongo.db.runs_new.find_one_or_404(
            {key: value},
            {"_id": 1,
             "name": 1,
             "number": 1,
             "{first}.{second}.{third}".format(first=top_level, 
                                               second=second_level,
                                               third=third_level): 1})
        app.logger.debug("Query result: %s "
                         % result)
        return flask.jsonify({"results": result})

class RunThirdLevelObjectID(Resource):
    def get(self, object_id, top_level, second_level, third_level):
        app.logger.debug(("Requesting {top_level}.{second_level}.{third_level} "
                          "data for run with object ID {object_id}").format(
                              top_level=top_level,
                              second_level=second_level,
                              object_id=object_id))
        return self._get_("_id", object_id, top_level,
                          second_level, third_level)


class RunThirdLevelRunID(Resource):
    def get(self, run_id, top_level, second_level, third_level):
        app.logger.debug(("Requesting {top_level}.{second_level}.{third_level} "
                          "data for run with run number {run_id}").format(
                              top_level=top_level,
                              second_level=second_level,
                              run_id=run_id))
        return self._get_("number", run_id, top_level,
                          second_level, third_level)


class RunThirdLevelTimestamp(Resource):
    def get(self, timestamp, top_level, second_level, third_level):
        app.logger.debug(("Requesting {top_level}.{second_level}.{third_level} "
                          "data for run with name {timestamp}").format(
                              top_level=top_level,
                              second_level=second_level,
                              timestamp=timestamp))
        return self._get_("name", timestamp, top_level,
                          second_level, third_level)


api.add_resource(RunThirdLevelObjectID,
                 ('/run/objectid/<ObjectId:object_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="run_object_id_thirdlevel")
api.add_resource(RunThirdLevelRunID,
                 ('/run/runnumber/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="run_run_id_thirdlevel")
api.add_resource(RunThirdLevelTimestamp,
                 ('/run/timestamp/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="run_timestamp_thirdlevel")

api.add_resource(RunThirdLevelObjectID,
                 ('/runs/objectid/<ObjectId:object_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="runs_object_id_thirdlevel")
api.add_resource(RunThirdLevelRunID,
                 ('/runs/runnumber/<int:run_id>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="runs_run_id_thirdlevel")
api.add_resource(RunThirdLevelTimestamp,
                 ('/runs/timestamp/<string:timestamp>/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>/'),
                 endpoint="runs_timestamp_thirdlevel")
