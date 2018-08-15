from flask_restful import Resource
from xenon_runsDB_api import util
from xenon_runsDB_api.app import app, api, mongo


class RunsProcessingVersion(Resource):
    def get(self, status, data_field=None):
        app.logger.debug('Requesting all runs with status: %s', status)
        if status == "not_processed":
            query = {"$not": {"$elemMatch": {"type": "processed"}},
                     "$elemMatch": {"type": "raw",
                                    "status": "transferred"}}
        elif status == "processing":
            query = {"$elemMatch": {"type": "processed",
                                    "status": "processing"}}
        elif status == "processed":
            # No processed data and raw data is transferring
            query = {"$elemMatch": {"type": "processed",
                                    "status": "processed"}}
        elif status == "transferring":
            # No processed data and raw data is transferring
            query = {"$not": {"$elemMatch": {"type": "processed"}},
                     "$elemMatch": {"type": "raw",
                                    "status": "transferring"}}
        query = {"data": query}
        results = util.get_data_single_top_level(query, data_field)
        app.logger.debug("results: %s" % results)
        return results


api.add_resource(RunsStatus, '/runs/status/<string:status>')
api.add_resource(RunsStatusPAXVersion, ('/runs/status/<string:status>/'
                                        ('pax_version/<string:pax_version>/'
                                         '<string:data_field>'))