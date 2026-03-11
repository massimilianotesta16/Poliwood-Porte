from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


collezioni_finiture = db.Table('collezioni_finiture',
    db.Column('id_collezione', db.Integer, db.ForeignKey('collezioni.id_collezione'), primary_key=True),
    db.Column('id_finitura', db.Integer, db.ForeignKey('finiture.id_finitura'), primary_key=True)
)

class Collezione(db.Model):
    __tablename__ = 'collezioni'
    id_collezione = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_collezione = db.Column(db.String(100), nullable=False)
    immagine_copertina = db.Column(db.String(255))
    tipologia = db.Column(db.String(50))
    
    modelli = db.relationship('Modello', backref='collezione', lazy=True)
    finiture = db.relationship('Finitura', secondary=collezioni_finiture, backref='collezioni')
    galleria = db.relationship('GalleriaImmagini', backref='collezione_riferimento', lazy=True)

class Finitura(db.Model):
    __tablename__ = 'finiture'
    id_finitura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_finitura = db.Column(db.String(100), nullable=False)
    immagine_texture = db.Column(db.String(255))

class Modello(db.Model):
    __tablename__ = 'modelli'
    id_modello = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_collezione = db.Column(db.Integer, db.ForeignKey('collezioni.id_collezione'))
    nome_modello = db.Column(db.String(100), nullable=False)
    immagine_modello = db.Column(db.String(255))

class ModelloVariante(db.Model):
    __tablename__ = 'modelli_varianti'
    id_modello = db.Column(db.Integer, db.ForeignKey('modelli.id_modello'), primary_key=True)
    id_variante = db.Column(db.Integer, db.ForeignKey('varianti.id_variante'), primary_key=True)
    immagine_variante = db.Column(db.String(255)) # L'attributo appeso al rombo!
    
    modello = db.relationship('Modello', backref='varianti_associate')
    variante = db.relationship('Variante', backref='modelli_associati')

class Variante(db.Model):
    __tablename__ = 'varianti'
    id_variante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_variante = db.Column(db.String(100), nullable=False) # Es. "Piena", "Vetro"

class Articolo(db.Model):
    __tablename__ = 'articoli'
    id_articolo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titolo = db.Column(db.String(200), nullable=False)
    sunto = db.Column(db.String(500))
    contenuto = db.Column(db.Text)
    immagine_copertina = db.Column(db.String(255))
    data_pubblicazione = db.Column(db.DateTime, default=datetime.utcnow)
    pubblicato = db.Column(db.Boolean, default=False)
    
    galleria = db.relationship('GalleriaImmagini', backref='articolo_riferimento', lazy=True)

class GalleriaImmagini(db.Model):
    __tablename__ = 'galleria_immagini'
    id_immagine = db.Column(db.Integer, primary_key=True, autoincrement=True)
    percorso_url = db.Column(db.String(255), nullable=False)
    testo_alt = db.Column(db.String(255))
    
    id_collezione = db.Column(db.Integer, db.ForeignKey('collezioni.id_collezione'), nullable=True)
    id_articolo = db.Column(db.Integer, db.ForeignKey('articoli.id_articolo'), nullable=True)
    
class Utente(db.Model):
    __tablename__ = 'utenti'
    id_utente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_utente = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)