from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tutor_nome = db.Column(db.String(100), nullable=False)
    tutor_contato = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="ativo")
    consultas = db.relationship("Consulta", backref="animal", lazy=True)
    exames = db.relationship("Exame", backref="animal", lazy=True)

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="agendada")
    diagnostico = db.Column(db.Text)
    tratamento = db.Column(db.Text)
    cirurgia = db.Column(db.Text)
    peso = db.Column(db.Float)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)

class Exame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    imagem_url = db.Column(db.String(200))
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
