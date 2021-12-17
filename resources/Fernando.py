from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify

dados = {
        'Nome': 'Fernando Emerson',
        'Idade': 22,
        'Telefone': '(21)98931-9729',
        'Status Code': '200, success'
        }

#classe que armazena e retorna o dicionário com os meus dados
class my_data(Resource):
    @jwt_required()
    def get(self):
        return dados


