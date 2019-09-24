from flask_sqlalchemy import SQLAlchemy
import os, sys, enum

db = SQLAlchemy()

tags = db.Table('tags',
    db.Column('receta_id', db.Integer, db.ForeignKey('receta.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
)


class Messurments(enum.Enum):
    mililiter = "ml"
    miligram = "mg"
    ounce = "oz"

class Category(enum.Enum):
    meet = "meet"
    grane = "grane"
    vedgetable = "vedgetable"
    dary = "dary"
    fruit = "fruit"
    nut = "nut"

class Market(enum.Enum):
    publix = "publix"
    walmart = "walmart"
    president = "president"
    whole_foods = "whole_foods"


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")

    def __repr__(self):
         return '<User %r>' % self.username


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Integer, nullable=False)
    talla = db.Column(db.Integer, nullable=False)
    alergia = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="profile")
    # recetas = db.relationship("Receta", back_populates="autor")

    def __repr__(self):
         return '<Profile %r>' % self.id

class Stock(db.Model):
    __tablename__ = 'stock'
    id=db.Column(db.Integer, primary_key=True)
    id_profile = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    quantity = db.Column(db.Float, nullable=False)
'''
class Receta_Ingrediente(db.Model):
    __tablename__ = 'receta_ingrediente'
    id=db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey('receta.id'))
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    quantity = db.Column(db.Float, nullable=False)
    messurment = db.Column(db.Enum(Messurments), nullable=False)
'''

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    calory = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(80), unique=False, nullable=False)
    # autor = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=True)
    relacion = db.relationship('Ingrediente', secondary=tags, backref=db.backref('ingredientes', lazy='dynamic'))
    def __repr__(self):
         return '<Receta %r>' % self.name

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.Enum(Category), nullable=False)
    calory = db.Column(db.Integer, nullable=False)
    prices = db.relationship("Price", backref="ingrediente")
    # stock = db.relationship("Stock", back_populates="id_ingrediente")

    def __repr__(self):
         return '<Ingrediente %r>' % self.name

class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.Integer, primary_key=True)
    market_name = db.Column(db.Enum(Market), nullable=False)
    price = db.Column(db.Float, nullable=False)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))

    def __repr__(self):
         return '<Price %r>' % self.market_name
