import flask
import flask_praetorian
from flask_restful import Resource
from xenon_runsDB_api.app import guard, app, api, mongo
from marshmallow import Schema, fields
from webargs.flaskparser import use_kwargs, use_args


class Root(Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


api.add_resource(Root, '/')


class SiteMap(Resource):
    def get(self):
        return flask.jsonify(
            {"routes": ['%s' % rule for rule in app.url_map.iter_rules()]})


api.add_resource(SiteMap, '/sitemap')


user_args = {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
}


class Login(Resource):
    @use_args(user_args, locations=["json"])
    def post(self, args):
        user = guard.authenticate(args["username"], args["password"])
        ret = {'access_token': guard.encode_jwt_token(user)}
        return flask.jsonify(ret)

api.add_resource(Login, '/login')


class RefreshToken(Resource):
    def get(self):
        old_token = guard.read_token_from_header()
        new_token = guard.refresh_jwt_token(old_token)
        ret = {'access_token': new_token}
        return flask.jsonify(ret)

api.add_resource(RefreshToken, "/refresh")


class AddUser(Resource):
    @use_args(user_args, locations=["json"])
    @flask_praetorian.roles_required('admin')
    def post(self, args):
        pass

api.add_resource(AddUser, '/adduser')