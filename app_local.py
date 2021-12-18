
from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.Fernando import my_data
from resources.user import Create, Login, Logout, UserAccountConfirm
from flask_jwt_extended import JWTManager

# Inicializa o Flask
app = Flask(__name__)

# caminho e nome do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configuração do access token
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'

# ativa a "lista negra" do jwt
app.config['JWT_BLACKLIST_ENABLE'] = True

#instância do restful (objeto que define as rotas)
api = Api(app)

#instância do JWT (gerenciador de credenciais, tokens)
jwt = JWTManager(app)

@app.route('/')
def index():
    return '<h1>RESTFul API - Teste prático'

# cria o banco de dados e todas as tabelas antes da primeira requisição 
# através da função "create_all"
@app.before_first_request
def make_database():
    db.create_all()

#verifica se um token está ou não na blacklist
@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST

# revoga o acesso do token que estiver na blacklist
@jwt.revoked_token_loader
def invalid_token(jwt_header, jwt_payload):
    return jsonify({'message': 'Você foi deslogado.'}), 401

# define as rotas e recursos
api.add_resource(my_data, '/Fernando')
api.add_resource(Create, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserAccountConfirm, '/accverification/<int:user_id>')

if __name__ == '__main__':
    from sql_alchemy import db
    # a lib sql_alchemy é importada aqui para que só seja criado o db 
    # quando executado o arquivo main
    db.init_app(app)
    app.run(debug=True) 