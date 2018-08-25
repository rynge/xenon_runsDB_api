from flask_restful import Resource
from xenon_runsDB_api.common import util
from xenon_runsDB_api.app import app, api, mongo

class RunsStatusInfo(Resource):
    def get(self):
        return """Supported status fields are: 
not_processed: Runs are are transferred, but not processed
processing: Runs are having been submitted for processing, but haven't completed yet
processed: Runs that have been processed
transferring: Runs that are transferring from LNGS and haven't been processed
"""


class RunsStatus(Resource):
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


class RunsStatusPAXVersion(Resource):
    def get(self, status, pax_version, data_field=None):
        app.logger.debug(('Requesting all runs with status: %s and '
                          'PAX version: %s'),
                         (status, pax_version))
        if status == "processing":
            query = {"$elemMatch": {"type": "processed",
                                    "status": "processing",
                                    "pax_version": pax_version}}
        elif status == "processed":
            query = {"$elemMatch": {"type": "processed",
                                    "status": "processed",
                                    "pax_version": pax_version}}
        results = util.get_data_single_top_level(query, data_field)
        app.logger.debug("results: %s" % results)
        return results


api.add_resource(RunsStatusInfo, '/runs/status')
api.add_resource(RunsStatus, '/runs/status/<string:status>')
api.add_resource(RunsStatusPAXVersion, ('/runs/status/<string:status>/'
                                        'pax_version/<string:pax_version>/'
                                         '<string:data_field>'))