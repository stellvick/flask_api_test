from os.path import abspath

from flask_restful import Resource, reqparse, request
from models.hotel_model import HotelModel
from utils.search import normalize_hotel_path_params, search_hotel_query

import sqlite3


class Hoteis(Resource):
    def __init__(self):
        self.path_params = reqparse.RequestParser()
        self.path_params.add_argument('cidade', type=str)
        self.path_params.add_argument('estrelas_min', type=float)
        self.path_params.add_argument('estrelas_max', type=float)
        self.path_params.add_argument('diaria_min', type=float)
        self.path_params.add_argument('diaria_max', type=float)
        self.path_params.add_argument('limit', type=int)
        self.path_params.add_argument('offset', type=int)

    @staticmethod
    def get():
        dados = request.args
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        params = normalize_hotel_path_params(**dados_validos)
        db_path = abspath('instance/banco.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        consulta = search_hotel_query(params)
        tupla = tuple([params[chave] for chave in params])
        resultado = cursor.execute(consulta, tupla)
        hoteis = []
        if not resultado:
            return {'message': 'Nenhum hotel encontrado'}, 404
        for linha in resultado:
            new_hotel = HotelModel(*linha).json()
            hoteis.append(new_hotel)
        return {'hoteis': hoteis}, 200
