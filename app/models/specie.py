import json

from app import db
from sqlalchemy.orm import relationship


class Specie(db.Model):
    """
    Specie identity class
    """
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    animals = relationship('Animal', backref='specie')

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        specie_object = {
            'name': self.name,
            'description': self.description,
            'price': self.price
        }
        return json.dumps(specie_object)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_species(cls):
        """
        :return: list with all species
        """
        return [str(specie) for specie in cls.query.all()]

    @classmethod
    def get_animals_count_by_name(cls, name):
        """
        Get animals count by specie name
        :param name:
        :return: number of animals
        """
        return len(cls.query.filter_by(name=name).first().animals)

    @classmethod
    def add_specie(cls, name, description, price):
        """
        Add new specie
        :param name:
        :param description:
        :param price:
        :return: new specie id
        """
        new_specie = cls(name, description, price)
        db.session.add(new_specie)
        db.session.commit()
        return new_specie.id

    @classmethod
    def get_specie(cls, specie_id):
        """
        Get specie by id
        :param specie_id:
        :return: specie object
        """
        return Specie.query.filter_by(id=specie_id).first()
