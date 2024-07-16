from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.hotel_model import HotelModel


class Hotel(Resource):
    def __init__(self):
        self.args = reqparse.RequestParser()
        self.args.add_argument('nome', type=str, required=True, help="Nome field cannot be left blank.")
        self.args.add_argument('estrelas', type=float, required=True, help="Estrelas field cannot be left blank.")
        self.args.add_argument('diaria', type=float, required=True, help="Diaria field cannot be left blank.")
        self.args.add_argument('cidade', type=str, required=True, help="Cidade field cannot be left blank.")

    @staticmethod
    def get(hotel_id: str):
        hotel = HotelModel.find_one(hotel_id)
        if hotel:
            return {"hoteis": [hotel.json()]}, 200
        return {'message': 'Hotel not found.'}, 404

    @jwt_required()
    def post(self, hotel_id: str):
        if HotelModel.find_one(hotel_id):
            return {'message': f'Hotel id {hotel_id} already exists.'}, 400
        data = self.args.parse_args()
        new_hotel = HotelModel(hotel_id, **data)
        try:
            new_hotel.save_hotel()
        except (Exception, ValueError):
            return {'message': f'An error occurred inserting the hotel. {new_hotel} - {Exception}'}, 500
        return {"hoteis": [new_hotel.json()]}, 201

    @jwt_required()
    def put(self, hotel_id: str):
        hotel = HotelModel.find_one(hotel_id)
        if hotel:
            try:
                hotel.update_hotel(**self.args.parse_args())
            except (Exception, ValueError):
                return {'message': 'An error occurred updating the hotel.'}, 500
            return {"hoteis": [hotel.json()]}, 200
        data = self.args.parse_args()
        new_hotel = HotelModel(hotel_id, **data)
        try:
            new_hotel.save_hotel()
        except (Exception, ValueError):
            return {'message': 'An error occurred inserting the hotel.'}, 500
        return {"hoteis": [new_hotel.json()]}, 200

    @staticmethod
    @jwt_required()
    def delete(hotel_id: str):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete()
            except (Exception, ValueError):
                return {'message': 'An error occurred deleting the hotel.'}, 500
            return {'message': 'Hotel deleted.'}, 200
        return {'message': 'Hotel not found.'}, 404
