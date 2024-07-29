from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.user_model import UserModel
from flask import make_response, render_template


class UserConfirm(Resource):
    @classmethod
    @jwt_required()
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.active = True
            user.save_user()
            headers = {'Content-Type': 'text/html'}
            return make_response(
                render_template(
                    'confirmation_success.html',
                    email=user.email,
                    usuario=user.login
                ),
                200,
                headers
            )
        return {"message": "User not found."}, 404
