import flask
from .app import app, mongo

def get_data_single_top_level(query, additional_top_level=None):
    top_level_fields = ["_id", "number", "name"]
    if isinstance(additional_top_level, list):
        top_level_fields = top_level_fields + additional_top_level
    elif isinstance(additional_top_level, str):
        top_level_fields.append(additional_top_level)
    print(type(top_level_fields))
    print(top_level_fields)
    desired_fields = {tlf: 1 
                      for tlf in top_level_fields}
    cursor = mongo.db.runs_new.find(
        query,
        desired_fields)  
    app.logger.debug('Requesting %s records' % cursor.count())
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