
#OBS: Método jwt_required define que é necessário autentificar-se para acessar
# o método referido

from flask_jwt_extended.utils import get_jwt
from flask_restful import Resource, reqparse
from models.user import user_model
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST
from flask import make_response, render_template
import re

# recebe os dados de login e senha que o usuário digitar, como argumentos
atr = reqparse.RequestParser()
atr.add_argument('login', type=str, required=True, help="O campo 'login' é obrigatório")
atr.add_argument('password', type=str, required=True, help="O campo 'password' é obrigatório")
atr.add_argument('email', type=str)
atr.add_argument('account_verification', type=bool)


class Create(Resource): #cria novo usuário
    #rota: /register/
    def post(self):

        # variável que armazena o login e senha
        user_data = atr.parse_args()
        login = user_data['login']

        # verifica se o login já existe
        if user_model.find_user_by_login(login):
            return {"message": f"O login {login} já existe, por favor escolha um diferente."}, 400

        # verifica se a senha contém ao menos 8 dígitos
        if len(user_data['password']) < 8:
             return {'message': 'Senha muito fraca, por favor digite uma senha com pelo menos 8 caracteres.'}, 400

        # verifica se usuário preencheu campo email
        if not user_data.get('email') or user_data.get('email') is None:
            return {'message': "O campo 'e-mail' precisa ser preenchido"}, 400
        
        # verifica se já existe esse email cadastrado
        if user_model.find_user_by_email(user_data['email']):
            return {"message": "O E-mail digitado já existe"}, 400

        # padrão regex para validar sintaxe do email
        r = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

        if not r.match(user_data.get('email')):
            return {"message": f"O e-mail {user_data.get('email')} é inválido, por favor digite um e-mail válido e tente novamente"}

        #instancia a classe modelo user_model que recebe login e senha
        user = user_model(**user_data)
        #garante que no momento do cadastro o status de verificação da conta é False
        user.account_verification = False
        #salva as configurações
        
        user.save_user()
        try:
            user.send_email_verification()
            return {'message': 'Usuário criado com sucesso!'}, 201
        except:
            return {'message': 'Houve algum problema ao enviar o email de confirmação, tente novamente'}


class Login(Resource):

    @classmethod
    def post(cls):
        user_data = atr.parse_args()
        user = user_model.find_user_by_login(user_data['login'])

        # método "safe_str_cmp" utilizado para fazer comparações de credenciais 
        # de forma mais segura 
        if user and safe_str_cmp(user.password, user_data['password']):
            if user.account_verification:
                token = create_access_token(identity=user.user_id)
                return {'token': token}, 200
            return {'message': 'É preciso verificar a conta para se conectar à API'}, 400
        return {'message': 'O usuário ou a senha está errado'}, 401


class Logout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # retorna o ID do token gerado na sessão (JWT token identifier)
        BLACKLIST.add(jwt_id) # variável constante do tipo set() p/ armazenar os ids
        return {'message': 'Você foi deslogado!'}, 200

class UserAccountConfirm(Resource):
    #/accverification/{user_id}
    @classmethod
    def get(cls, user_id):
        user = user_model.find_user_by_id(user_id)

        if not user:
            return {'message': f'Usuário não encontrado, verifique se o userid {user_id} está correto'}, 404

        user.account_verification = True
        user.save_user()
        # return {'message': 'Usuário confirmado com sucesso!'}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("confirm_page.html"), 200, headers)





