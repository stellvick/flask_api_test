from flask_restful import Resource, reqparse

from models.user_model import UserModel


class UserRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('login',
                                 type=str,
                                 required=True,
                                 help="This login cannot be left blank!"
                                 )
        self.parser.add_argument('senha',
                                 type=str,
                                 required=True,
                                 help="This senha cannot be left blank!"
                                 )
        self.parser.add_argument('active',
                                 type=bool,
                                 required=False,
                                 )
        self.parser.add_argument('email',
                                 type=str,
                                 required=True,
                                 help="This email cannot be left blank!"
                                 )

    def post(self):
        data = self.parser.parse_args()
        if not data.get('email') or data.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400
        if UserModel.find_by_email(data.get('email')):
            return {"message": f"User {data.get('email')} already exists."}, 400
        if UserModel.find_by_username(data.get('login')):
            return {"message": f"User {data.get('login')} already exists."}, 400
        user = UserModel(**data)
        user.active = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except (Exception, ValueError):
            user.delete_user()
            return {"message": f"An error occurred creating the user. {Exception} {ValueError}"}, 500
        return {"message": "User created successfully."}, 201
