from . import app, mongo


def get_data_single_top_level(query, top_level_field):
    cursor = mongo.db.runs_new.find({top_level_field: query})
    app.logger.debug('Requesting %s records' % cursor.count())
    return [x for x in cursor]