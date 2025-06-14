from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#* Modelo de Login
class Login(UserMixin, db.Model):
    __tablename__ = 'login'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)  #* Armazena senhas com hash
    nome_usuario = db.Column(db.String(100), nullable=False)

    #* Relacionamentos
    contas = db.relationship('Conta', backref='login', cascade="all, delete", lazy=True)
    cursos = db.relationship('Curso', backref='login', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<Login {self.nome_usuario}>"
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)

#* Modelo de Conta
class Conta(db.Model):
    __tablename__ = 'contas'

    id = db.Column(db.Integer, primary_key=True)
    id_login = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    site_conta = db.Column(db.String(255), nullable=False)
    email_conta = db.Column(db.String(255), nullable=False)
    senha_conta = db.Column(db.String(255), nullable=False)  #* Armazena senhas com hash

    #* Relacionamentos
    cursos = db.relationship('Curso', backref='conta', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<Conta {self.site_conta}>"

#* Modelo de Curso
class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    id_login = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    id_conta = db.Column(db.Integer, db.ForeignKey('contas.id'), nullable=False)
    nome_curso = db.Column(db.String(255), nullable=False)
    descricao_curso = db.Column(db.Text, nullable=True)
    imagem_curso = db.Column(db.LargeBinary, nullable=True)  #* Imagem do curso

    def __repr__(self):
        return f"<Curso {self.nome_curso}>"