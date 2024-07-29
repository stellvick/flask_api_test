import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
from alchemy import db
from flask import url_for, request
from requests import post
from utils.constants import MAIL_URL, MAIL_KEY, MAIL_FROM, MAIL_USER, MAIL_PASSWORD


class UserModel(db.Model):
    __tablename__ = 'usuarios'

    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), unique=True, nullable=False)
    senha = db.Column(db.String(40), nullable=False)
    active = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(80), nullable=False)

    def __init__(self, login: str, senha: str, active: bool, email: str):
        self.login = login
        self.senha = senha
        self.active = active
        self.email = email

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'active': self.active,
            'email': self.email
        }

    @classmethod
    def find_one(cls, user_id: str):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_username(cls, login: str):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email: str):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def send_confirmation_email(self):
        try:
            msg = EmailMessage()
            link = request.url_root[:-1] + url_for('confirmacao', user_id=self.user_id)
            msg['subject'] = "Confirmação de Cadastro"
            msg['from'] = Address("Hotelaria", "no-reply", MAIL_FROM)
            msg['to'] = (Address("Usuário", self.login, self.email),)
            msg.set_content(f"Seja bem-vindo ao Hotelaria! Para confirmar seu cadastro, clique no link: {link}")
            msg.add_alternative(f"""\
            <html>
                <head></head>
                <body>
                    <p>Seja bem-vindo ao Hotelaria! Para confirmar seu cadastro, clique no link:</p>
                    <a href="{link}"></a>
                </body>
            </html>
            """, subtype='html')
            server = smtplib.SMTP('smtp.mailgun.org', 587)
            server.starttls()
            server.login(MAIL_USER, MAIL_PASSWORD)
            with server as s:
                s.send_message(msg)
        except Exception as e:
            return e
