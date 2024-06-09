from pacote.ext.database import db


class Adm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    whatsapp = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.nome


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    escolaridade = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    anexo = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.nome
