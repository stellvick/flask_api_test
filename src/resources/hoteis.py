from flask_restful import Resource
from models.hotel_model import HotelModel
from utils.constants import hoteis


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}
