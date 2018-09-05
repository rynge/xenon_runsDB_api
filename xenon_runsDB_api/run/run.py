import flask
import flask_praetorian
from flask_restful import Resource
from xenon_runsDB_api.app import app, api, config, mongo
from xenon_runsDB_api.common.util import result_formatting


"""
Deleting, getting, inserting, the entire document for 
a run given a unique identifier for the desired run. In this 
case there are three possible identifiers the database specific
document or object ID, the run number (or run id), 
and the timestamp in YYMMDD_HHMM format.
"""


class Run(Resource):
    """
    Super class that provides semi-hidden generalized versions of functions
    needed to GET and DELETE.

    TODO: Finish POST function for run documents. 
    """

    def __init__(self):
        self.mongodb = mongo.db[config["runsDB"]["database_name"]]

    @flask_praetorian.roles_required('user')
    def _get_(self, key, value, top_level=None, second_level=None,
              third_level=None):
        """
        Generalized GET function to make DB retrieval calls, including 
        filter down to the third level. 

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
            If query successful: JSON object of the run document
            If not: returns 404
        """
        
        app.logger.debug(("key {}, value {}, top_level {}, second_level {}, "
                          "third_level {}").format(key, value, top_level, 
                                                   second_level, third_level))
        if top_level:
            limited_view = config["runsDB"]["views"]["limited_view"]
            if not second_level:
                limited_view.update({top_level: 1})
            if second_level:
                limited_view.update({"{first}.{second}".format(
                    first=top_level, 
                    second=second_level): 1})
            if third_level:
                limited_view.update({"{first}.{second}.{third}".format(
                    first=top_level, 
                    second=second_level,
                    third=third_level): 1})
            result = self.mongodb.find_one_or_404({key: value}, limited_view)
            result = result_formatting(result, top_level,
                                       second_level, third_level)
        else:
            result = self.mongodb.find_one_or_404({key: value})
        app.logger.debug("Query result: %s "
                         % result)
        return flask.jsonify({"results": result})
    
    @flask_praetorian.roles_required('admin')
    def _delete_(self, key, value):
        """
        Generalized DELETE function to make DB delete calls

        Args:
            key (string): Key in the run document
            value (string, int, BSON object ID): Search limit

        Returns:
            Empty string and status 204
        """
        self.mongodb.delete_one({key: value})
        return '', 204
    
    @flask_praetorian.roles_required('production', 'admin')
    def _post_(self, doc):
        """
        TODO: Add webargs to parse a preliminary JSON doc needed to add a run
        doc to the runsDB

        Function to add a run document

        Args:
            doc (JSON): Run document to be added
        """
        pass


class RunObjectID(Run):
    """
    Inherited class from run that provides interface when using object IDs
    """
    def get(self, object_id, top_level=None, second_level=None,
            third_level=None):
        return self._get_("_id", object_id, top_level, second_level, 
                          third_level)

    def delete(self, object_id):
        return self._delete_("_id", object_id)


class RunRunNumber(Run):
    """
    Inherited class from run that provides interface when using the run number
    """
    def get(self, run_number, top_level=None, second_level=None,
            third_level=None):
        return self._get_("number", run_number, top_level, second_level, 
                          third_level)

    def delete(self, run_number):
        return self._delete_("number", run_number)


class RunTimestamp(Run):
    """
    Inherited class from run that provides interface when using the run start
    timestamp
    """
    def get(self, timestamp, top_level=None, second_level=None,
            third_level=None):
        return self._get_("name", timestamp, top_level, second_level, 
                          third_level)

    def delete(self, timestamp):
        return self._delete_("name", timestamp)


# Adding routes according what identifier is used.
api.add_resource(RunObjectID,
                 '/run/objectid/<ObjectId:object_id>/',
                 '/run/objectid/<ObjectId:object_id>/filter/<string:top_level>',
                 ('/run/objectid/<ObjectId:object_id>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/run/objectid/<ObjectId:object_id>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="run_object_id")
api.add_resource(RunRunNumber,
                 '/run/runnumber/<int:run_number>/',
                 '/run/runnumber/<int:run_number>/filter/<string:top_level>',
                 ('/run/runnumber/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/run/runnumber/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="run_run_number")
api.add_resource(RunRunNumber,
                 '/run/number/<int:run_number>/',
                 '/run/number/<int:run_number>/filter/<string:top_level>',
                 ('/run/number/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/run/number/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="run_number")
api.add_resource(RunTimestamp,
                 '/run/timestamp/<string:timestamp>/',
                 '/run/timestamp/<string:timestamp>/filter/<string:top_level>',
                 ('/run/timestamp/<string:timestamp>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/run/timestamp/<string:timestamp>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="run_timestamp")
api.add_resource(RunTimestamp,
                 '/runs/name/<string:timestamp>/',
                 '/run/name/<string:timestamp>/filter/<string:top_level>',
                 ('/run/name/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/run/name/<string:timestamp>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="run_timestamp_name")

# Including the path for runs. Just in case we change our
# mind down the road
api.add_resource(RunObjectID,
                 '/runs/objectid/<ObjectId:object_id>/',
                 '/runs/objectid/<ObjectId:object_id>/filter/<string:top_level>',
                 ('/runs/objectid/<ObjectId:object_id>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/runs/objectid/<ObjectId:object_id>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="runs_object_id")
api.add_resource(RunRunNumber,
                 '/runs/runnumber/<int:run_number>/',
                 '/runs/runnumber/<int:run_number>/filter/<string:top_level>',
                 ('/runs/runnumber/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/runs/runnumber/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="runs_run_number")
api.add_resource(RunRunNumber,
                 '/runs/number/<int:run_number>/',
                 '/runs/number/<int:run_number>/filter/<string:top_level>',
                 ('/runs/number/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/runs/number/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="runs_number")
api.add_resource(RunTimestamp,
                 '/runs/timestamp/<string:timestamp>/',
                 '/runs/timestamp/<string:timestamp>/filter/<string:top_level>',
                 ('/runs/timestamp/<string:timestamp>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/runs/timestamp/<string:timestamp>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="runs_timestamp")
api.add_resource(RunTimestamp,
                 '/runs/name/<string:timestamp>/',
                 '/runs/name/<string:timestamp>/filter/<string:top_level>',
                 ('/runs/name/<int:run_number>/filter/'
                  '<string:top_level>/<string:second_level>/'),
                 ('/runs/name/<string:timestamp>/filter/'
                  '<string:top_level>/<string:second_level>/'
                  '<string:third_level>'),
                 endpoint="runs_timestamp_name")
# Path for insert new run doc with either /run/ or /runs
api.add_resource(Run,
                 "/run/insert",
                 "/runs/insert",
                 endpoint="run_insert")

