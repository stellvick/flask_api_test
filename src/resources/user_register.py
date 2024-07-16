from flask_restful import Resource, reqparse

from models.user_model import UserModel


class UserRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('login',
                                 type=str,
                                 required=True,
                                 help="This field cannot be left blank!"
                                 )
        self.parser.add_argument('senha',
                                 type=str,
                                 required=True,
                                 help="This field cannot be left blank!"
                                 )

    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['login']):
            return {"message": f"User {data['login']} already exists."}, 400
        user = UserModel(**data)
        try:
            user.save_user()
        except (Exception, ValueError):
            return {"message": f"An error occurred creating the user. {Exception} {ValueError}"}, 500
        return {"message": "User created successfully."}, 201
