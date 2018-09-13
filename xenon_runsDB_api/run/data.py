import flask
import flask_praetorian
from flask_restful import Resource
from marshmallow import Schema, fields
from webargs.flaskparser import use_kwargs, use_args
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api, mongo, config


# webargs/Marshmellow de/serialization object definition
# We require the same fields as the DAQ to be present.
data_args = {
    # String with all file checksums
    "checksum": fields.String(required=True),
    # date time in iso format
    "creation_time": fields.DateTime(format="iso", required=True),
    # Where the data was created
    "creation_place": fields.String(),
    # Where the data is located 
    "host": fields.String(required=True),
    # Location of the data on the host
    "location": fields.String(required=True),
    # Type of data data
    "type": fields.String(required=True),
    # What the status is
    "status": fields.String(required=True),
    # For raw data only, where the data is located
    "rse": fields.List(fields.String()),
    # For raw data only, what the status 
    "rule_info": fields.List(fields.String()),
    # hash used by strax to identify processing version
    "strax_hash": fields.String(),
    # pax version that was used for processing
    "pax_version": fields.String()
}


class RunData(Resource):

    def __init__(self):
        self.mongodb = mongo.db[config["runsDB"]["database_name"]]
        self.views = {"data": 1}.update(
            config["runsDB"]["views"]["limited_view"])

    def _get_(self, key, value, data_type=None):
        """
        
        """
        app.logger.debug("Requesting data for run with %s %s"
                         % (key, value))
        app.logger.debug("views %s" % self.views)
        result = self.mongodb.find_one_or_404({key: value}, self.views)
        app.logger.debug("Query results: %s", result)
        if data_type:
            limited_data = [do for do in result["data"] 
                            if do["type"] == data_type]
            result["data"] = limited_data
        app.logger.debug("Keys for result: %s" % result.keys())
        return result
    
    def _post_data_(self, key, value, data):
        """
        
        """
        run_doc_before = self.mongodb.find_one_or_404({key: value}, self.views)
        run_doc_before = util.result_formatting(run_doc_before, "data")
        data = util.fix_marshmallow_decoding(data)
        self.mongodb.find_one_and_update({key: value}, 
                                         {"$push": {"data": data}})
        run_doc_after = self.mongodb.find_one_or_404({key: value}, self.views)
        run_doc_after = util.result_formatting(run_doc_after, "data")
        return flask.jsonify({"previous_run_doc": run_doc_before,
                              "new_run_doc": run_doc_after})

    def _delete_(self, key, value, data):
        """
        
        """
        run_doc_before = self.mongodb.find_one_or_404({key: value}, self.views)
        run_doc_before = util.result_formatting(run_doc_before, "data")
        data = util.fix_marshmallow_decoding(data)
        app.logger.debug("Data being deleted: %s", data)
        self.mongodb.find_one_and_update({key: value},
            {"$pull": {"data": data}})
        run_doc_after = self.mongodb.find_one_or_404({key: value}, self.views)
        run_doc_after = util.result_formatting(run_doc_after, "data")
        return flask.jsonify({"previous_run_doc": run_doc_before,
                              "new_run_doc": run_doc_after})



class RunObjectIDData(RunData):
    def get(self, object_id, data_type=None):
        result = self._get_("object_id", object_id, data_type)
        return flask.jsonify({"results": result})
    
    @use_kwargs(data_args, locations=["json"])
    def post(self, object_id, **data):
        return self._post_data_("_id", object_id, data)

    @use_kwargs(data_args, locations=["json"])
    def delete(self, run_number, **data):
        return self._delete_("_id", object_id, data)


class RunRunNumberData(RunData):
    def get(self, run_number, data_type=None):
        result = self._get_("number", run_number, data_type)
        return flask.jsonify({"results": result})
    
    @use_kwargs(data_args, locations=["json"])
    def post(self, run_number, **data):
        return self._post_data_("number", run_number, data)

    @use_kwargs(data_args, locations=["json"])
    def delete(self, run_number, **data):
        return self._delete_("number", run_number, data)


class RunTimestampData(RunData):
    def get(self, timestamp, data_type=None):
        result = self._get_("name", timestamp, data_type)
        return flask.jsonify({"results": result})
    
    @use_kwargs(data_args, locations=["json"])
    def post(self, timestamp, **data):
        return self._post_data_("name", timestamp, data)

    @use_kwargs(data_args, locations=["json"])
    def delete(self, timestamp, **data):
        return self._delete_("name", timestamp, data)


api.add_resource(RunObjectIDData,
                 '/run/objectid/<ObjectId:object_id>/data/',
                 endpoint="run_object_id_data_no_type")
api.add_resource(RunObjectIDData,
                 '/run/objectid/<ObjectId:object_id>/data/<string:data_type>/',
                 endpoint="run_object_id_data",
                 methods=['GET'])

api.add_resource(RunObjectIDData,
                 '/runs/objectid/<ObjectId:object_id>/data/',
                 endpoint="runs_object_id_data_no_type")
api.add_resource(RunObjectIDData,
                 '/runs/objectid/<ObjectId:object_id>/data/<string:data_type>/',
                 endpoint="runs_object_id_data",
                 methods=['GET'])


api.add_resource(RunRunNumberData,
                 '/run/number/<int:run_number>/data/',
                 endpoint="run_number_data_no_type")
api.add_resource(RunRunNumberData,
                 '/run/number/<int:run_number>/data/<string:data_type>/',
                 endpoint="run_number_data",
                 methods=['GET'])

api.add_resource(RunRunNumberData,
                 '/run/runnumber/<int:run_number>/data/',
                 endpoint="run_run_number_data_no_type")
api.add_resource(RunRunNumberData,
                 '/run/runnumber/<int:run_number>/data/<string:data_type>/',
                 endpoint="run_run_number_data",
                 methods=['GET'])       

api.add_resource(RunRunNumberData,
                 '/runs/number/<int:run_number>/data/',
                 endpoint="runs_number_data_no_type")
api.add_resource(RunRunNumberData,
                 '/runs/number/<int:run_number>/data/<string:data_type>/',
                 endpoint="runs_number_data",
                 methods=['GET'])

api.add_resource(RunRunNumberData,
                 '/runs/runnumber/<int:run_number>/data/',
                 endpoint="runs_run_number_data_no_type")
api.add_resource(RunRunNumberData,
                 '/runs/runnumber/<int:run_number>/data/<string:data_type>/',
                 endpoint="runs_run_number_data",
                 methods=['GET'])


api.add_resource(RunTimestampData,
                 '/run/timestamp/<string:timestamp>/data/',
                 endpoint="run_timestamp_data_no_type")
api.add_resource(RunTimestampData,
                 '/run/timestamp/<string:timestamp>/data/<string:data_type>/',
                 endpoint="run_timestamp_data",
                 methods=['GET'])

api.add_resource(RunTimestampData,
                 '/run/name/<string:timestamp>/data/',
                 endpoint="run_name_timestamp_data_no_type")
api.add_resource(RunTimestampData,
                 '/run/name/<string:timestamp>/data/<string:data_type>/',
                 endpoint="run_name_timestamp_data",
                 methods=['GET'])

api.add_resource(RunTimestampData,
                 '/runs/timestamp/<string:timestamp>/data/',
                 endpoint="runs_timestamp_data_no_type")
api.add_resource(RunTimestampData,
                 '/runs/timestamp/<string:timestamp>/data/<string:data_type>/',
                 endpoint="runs_timestamp_data",
                 methods=['GET'])

api.add_resource(RunTimestampData,
                 '/runs/name/<string:timestamp>/data/',
                 endpoint="runs_name_timestamp_data_no_type")
api.add_resource(RunTimestampData,
                 '/runs/name/<string:timestamp>/data/<string:data_type>/',
                 endpoint="runs_name_timestamp_data",
                 methods=['GET'])
