from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user_model import UserModel
from utils.security import safe_str_cmp

parser = reqparse.RequestParser()
parser.add_argument('login',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )
parser.add_argument('senha',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = parser.parse_args()
        user = UserModel.find_by_username(data['login'])
        if user and safe_str_cmp(user.senha, data['senha']):
            if user.active:
                token = create_access_token(identity=user.user_id)
                return {
                    "message": "Logged in successfully.",
                    "token": token
                }, 200
            return {"message": "User not active."}, 400
        return {"message": "Invalid credentials."}, 401