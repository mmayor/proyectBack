from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# from eralchemy import render_er

db = SQLAlchemy()

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }


class PivRecIng(db.Model):
    __tablename__ = 'pivRecIng'
    id=Column(Integer, primary_key=True)
    idFallower = Column(Integer, ForeignKey('person.fallowersId'))
    idFallowing = Column(Integer, ForeignKey('person.fallowingId'))

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
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = db.relationship("User", back_populates="profile")

    def __repr__(self):
         return '<Profile %r>' % self.id

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    caloria = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
         return '<Receta %r>' % self.name


class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    tipo = db.Column(db.String(80), unique=False, nullable=False)
    caloria = db.Column(db.Integer, nullable=False)

    def __repr__(self):
         return '<Receta %r>' % self.name

