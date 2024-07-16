from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.user_model import UserModel


class Usuario(Resource):
    @staticmethod
    def get(user_id: str):
        user = UserModel.find_one(user_id)
        if user:
            return {"usuario": [user.json()]}, 200
        return {'message': f'User {user_id} not found.'}, 404

    @staticmethod
    @jwt_required()
    def delete(user_id: str):
        user = UserModel.find_one(user_id)
        if user:
            try:
                user.delete_user()
            except (Exception, ValueError):
                return {'message': f'An error occurred deleting the user. {Exception} {ValueError}'}, 500
            return {'message': 'User deleted.'}, 200
        return {'message': f'User {user_id} not found.'}, 404
