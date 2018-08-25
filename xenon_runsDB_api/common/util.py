import flask
from xenon_runsDB_api.app import app, mongo

def get_data_single_top_level(query, additional_top_level=None):
    """
    Helper function for larger queries that will produce a list of output
    
    Args:
        query (dict): Query passed to PyMongo
        additional_top_level (str or list of str): Fields to add to returned
                                                   query

    Returns:
        JSON with "results" key that has list of run docs with limited 
        contents
    """
    # Reducing fields that will be returned by MongoDB
    # Only return the Object ID, run number, and run name by default
    # Add the desired fields either as a list of str
    top_level_fields = ["_id", "number", "name"]
    if isinstance(additional_top_level, list):
        top_level_fields = top_level_fields + additional_top_level
    elif isinstance(additional_top_level, str):
        top_level_fields.append(additional_top_level)
    else:
        return flask.abort(404, "Please pass a string or list of fields")
    desired_fields = {tlf: 1 
                      for tlf in top_level_fields}
    cursor = mongo.db.runs_new.find(
        query,
        desired_fields)  
    app.logger.debug('Requesting %s records' % cursor.count())
    # Need to convert cursor to list
    results = [x for x in cursor]
    app.logger.debug("results %s" % results)
    return flask.jsonify({"results": results})

def get_result_ready(result, top_level, second_level):
    """

    """
    if (isinstance(result[top_level], list) or
        isinstance(result[top_level], tuple)):
        filtered_results = [record[second_level]
                            for record in result[top_level]]
        return filtered_results
    if isinstance(result[top_level], dict):
        return result[top_level][second_level]
    if not (isinstance(result[top_level], list) or
            isinstance(result[top_level], tuple) or
            isinstance(result[top_level], dict)):
        return flask.abort(404)