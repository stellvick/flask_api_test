from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel
from utils.search import normalize_hotel_path_params

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

    def get(self):
        dados = self.path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        params = normalize_hotel_path_params(**dados_validos)
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        if not params.get('cidade'):
            consulta = "SELECT * FROM hoteis WHERE (estrelas >= ? and estrelas <= ?) " \
                       "and (diaria >= ? and diaria <= ?) LIMIT ? OFFSET ?"
        else:
            consulta = "SELECT * FROM hoteis WHERE (estrelas >= ? and estrelas <= ?) " \
                       "and (diaria >= ? and diaria <= ?) and cidade = ? LIMIT ? OFFSET ?"
        tupla = tuple([params[chave] for chave in params])
        resultado = cursor.execute(consulta, tupla)
        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })
        return {'hoteis': hoteis}, 200
