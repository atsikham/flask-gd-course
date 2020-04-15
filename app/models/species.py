from app import db
from sqlalchemy.orm import relationship


class Species(db.Model):
    """
    Species identity class
    """
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    animals = relationship('Animal', backref='species')

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def __str__(self):
        return self.name

    @classmethod
    def get_all_species(cls):
        """
        :return: list with all species
        """
        return [str(species) for species in cls.query.all()]

    @classmethod
    def get_animals_count_by_name(cls, name):
        """
        Get animals count by species name
        :param name:
        :return: number of animals
        """
        return len(cls.query.filter_by(name=name).first().animals)

    @classmethod
    def add_species(cls, name, description, price):
        """
        Add new species
        :param name:
        :param description:
        :param price:
        :return: new species id
        """
        new_species = cls(name, description, price)
        db.session.add(new_species)
        db.session.commit()
        return new_species.id

    @classmethod
    def get_species(cls, species_id):
        """
        Get species by id
        :param species_id:
        :return: species object
        """
        return Species.query.filter_by(id=species_id).first()
