from flask_restful import Resource, reqparse

from models.hotel_model import HotelModel
from utils.constants import hoteis


class Hotel(Resource):
    def __init__(self):
        self.args = reqparse.RequestParser()
        self.args.add_argument('nome', type=str, required=True, help="Nome field cannot be left blank.")
        self.args.add_argument('estrelas', type=float, required=True, help="Estrelas field cannot be left blank.")
        self.args.add_argument('diaria', type=float, required=True, help="Diaria field cannot be left blank.")
        self.args.add_argument('cidade', type=str, required=True, help="Cidade field cannot be left blank.")

    def get(self, hotel_id: str):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel, 200
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id: str):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id {hotel_id} already exists.'}, 400
        data = self.args.parse_args()
        new_hotel = HotelModel(hotel_id, **data)
        try:
            new_hotel.save_hotel()
        except (Exception, ValueError):
            return {'message': f'An error occurred inserting the hotel. {new_hotel} - {Exception}'}, 500
        return new_hotel, 201

    def put(self, hotel_id: str):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id {hotel_id} already exists.'}, 400
        data = self.args.parse_args()
        new_hotel = HotelModel(hotel_id, **data)
        try:
            new_hotel.save_hotel()
        except (Exception, ValueError):
            return {'message': 'An error occurred inserting the hotel.'}, 500
        return new_hotel, 200

    @staticmethod
    def delete(hotel_id: str):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            try:
                hoteis.remove(hotel)
            except (Exception, ValueError):
                return {'message': 'An error occurred deleting the hotel.'}, 500
            return {'message': 'Hotel deleted.'}, 200
        return {'message': 'Hotel not found.'}, 404
