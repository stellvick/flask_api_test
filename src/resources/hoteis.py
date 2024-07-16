from flask_restful import Resource
from models.hotel_model import HotelModel
from utils.constants import hoteis


class Hoteis(Resource):
    @staticmethod
    def get():
        return {'hoteis': [hotel.json() for hotel in HotelModel.find_all()]}
