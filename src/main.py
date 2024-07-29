import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, jsonify
from flask_restful import Api
from BLACKLIST import BLACKLIST
from exceptions.internal_error import InternalError
from exceptions.invalid_usage import InvalidUsage
from resources.hoteis import Hoteis
from resources.hotel import Hotel
from resources.site import Site
from resources.sites import Sites
from resources.user_confirm import UserConfirm
from resources.user_login import UserLogin
from resources.user_logout import UserLogout
from resources.user_register import UserRegister
from resources.usuario import Usuario
from flask_jwt_extended import JWTManager

sentry_sdk.init(
    dsn="https://042e6987e11572304d823b60c6cc3d0a@o4507656610447360.ingest.us.sentry.io/4507656613199872",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[FlaskIntegration(
        transaction_style="url"
    )]
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ChaveSecreta'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)

jwt = JWTManager(app)


@app.before_request
def cria_banco():
    app.before_request_funcs[None] = [cria_banco]
    db.create_all()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(InternalError)
def handle_exception(error):
    response = jsonify({'message': 'An internal error has occurred.'})
    response.status_code = 500
    return response


@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Usuario, '/user/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')

if __name__ == '__main__':
    from alchemy import db

    db.init_app(app)
    app.run(port=8000, debug=True)
