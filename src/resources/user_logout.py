from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from BLACKLIST import BLACKLIST


class UserLogout(Resource):
    @staticmethod
    @jwt_required()
    def post():
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
