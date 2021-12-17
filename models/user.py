from sql_alchemy import db
from flask import request, url_for
import yagmail
from email_config import sender_email, password


class user_model(db.Model):
    __tablename__ = 'users'

    # cria as colunas user id, login, senha e email
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    account_verification = db.Column(db.Boolean, default=False)

    def __init__(self, login, password, email, account_verification):
        self.login = login
        self.password = password
        self.email = email
        self.account_verification = account_verification

    def send_email_verification(self):
        #recupera, dinamicamente, a url que direciona ao link de verificação da conta
        url = request.url_root[:-1] + url_for('useraccountconfirm', user_id=self.user_id)

        contents = f'<html><p>Olá! Tudo bem? Para confirmar o seu cadastro basta clicar neste link: <a href="{url}">Confirmar Conta</a></p></html>'

        try:
            #initializing the server connection
            yag = yagmail.SMTP(user=sender_email, password=password)
            #sending the email
            yag.send(to=self.email, subject='Confirmação de conta', contents=contents)
            return {"message": f"Verifique o e-mail enviado para {self.email} e confirme o cadastro!"}, 201
        except:
            return {"message": f"Não foi possível enviar o e-mail de confirmação, verifique se o mesmo foi digitado corretamente"}, 401

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'account_verification': self.account_verification
        }
    
    @classmethod
    def find_user_by_id(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_user_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_user_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None 

    
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


