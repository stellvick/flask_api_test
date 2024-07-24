from werkzeug.exceptions import UnsupportedMediaType
from flask_restful import Resource, reqparse, request
from flask import jsonify
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

    @staticmethod
    def get():
        dados = request.args
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
        if not resultado:
            return {'message': 'Nenhum hotel encontrado'}, 404
        for linha in resultado:
            new_hotel = jsonify({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })
            hoteis.append(new_hotel)
        return {'hoteis': hoteis}, 200
