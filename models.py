from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)



class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules = ('-heropowers.hero')


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('HeroPower', back_populates='hero')

    def _repr_(self):
        return f'<Hero {self.name} aka {self.super_name}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    serialize_rules = ('-heropowers.power')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('HeroPower', back_populates='power')

    def _repr_(self):
        return f'<Hero {self.name} aka {self.description}>'




class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropowers'
    serialize_rules = ('-hero.powers', '-power.heroes')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10))
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']  
        if strength not in valid_strengths:
            raise AssertionError("invalid strength value")
        return strength