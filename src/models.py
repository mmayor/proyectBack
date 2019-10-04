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


    def serializeProfiles(self):
            return {
             "id": self.id,
             "peso": self.peso,
             "talla": self.talla,
             "alergia": self.alergia,
             "user_id": self.user_id
            }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")

    def __repr__(self):
         return '<User %r>' % self.username

    def serializeUsers(self):
        return {
            "id":self.id,
            "username": self.username,
            "email": self.email,
            # "profile":   (lambda x: x.serializeProfiles(), self.profile)
            "profile": self.profile.serializeProfiles()
}



class Stock(db.Model):
    __tablename__ = 'stock'
    id=db.Column(db.Integer, primary_key=True)
    id_profile = db.Column(db.Integer, db.ForeignKey('profile.id'))
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    quantity = db.Column(db.Float, nullable=False)


    def serializeStocks(self):
            return {
             "id": self.id,
             "id_profile": self.id_profile,
             "id_ingrediente": self.id_ingrediente,
             "quantity": self.quantity
            }


class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    calory = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(80), unique=False, nullable=False)
    # autor = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=True)
    guianew = db.Column(db.Text(), unique=False, nullable=False)
    ingrediente = db.relationship('Ingrediente', secondary=tags, backref=db.backref('newTags', lazy='dynamic'))
    def __repr__(self):
         return '<Receta %r>' % self.name

    def serializeReceta(self):
            return {
             "id": self.id,
             "name": self.name,
             "calory": self.calory,
             "guianew": self.guianew,
             #"prices": self.prices,
             "ingredientesTemp": list(map(lambda x: x.serializeIngrediente(), self.ingrediente)),

            }


class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.Enum(Category), nullable=False)
    calory = db.Column(db.Integer, nullable=False)
#    receta = db.relationship('Receta', secondary=tags, backref='ingrediente')
    prices = db.relationship("Price", backref="ingrediente")
    stock = db.relationship("Stock", backref="ingrediente")

    def __repr__(self):
         return '<Ingrediente %r>' % self.name

    def serializeIngrediente(self):
            return {
             "id": self.id,
             "name": self.name,
             "calory": self.calory,
             #"prices": self.prices,
             "stocksTemp": list(map(lambda x: x.serializeStocks(), self.stock)),
             "preciosTemp": list(map(lambda x: x.serializePrecios(), self.prices)),
            }

class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.Integer, primary_key=True)
    market_name = db.Column(db.Enum(Market), nullable=False)
    price = db.Column(db.Float, nullable=False)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))

    def __repr__(self):
         return '<Price %r>' % self.market_name


    def serializePrecios(self):
            return {
             "id": self.id,
             "market_name": self.market_name.name,
             "price": self.price,
             "id_ingrediente": self.id_ingrediente
            }
