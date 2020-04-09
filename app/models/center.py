import json

from app import db
from sqlalchemy.orm import relationship


class Center(db.Model):
    """
    Center model class that describes shop clients
    """
    __tablename__ = 'centers'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250), nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    animals = relationship('Animal', backref='center')
    access_entries = relationship('Access', backref='center')

    def __init__(self, address, login, password):
        self.address = address
        self.login = login
        self.password = password

    def __repr__(self):
        center_object = {
            'address': self.address,
            'login': self.login
        }
        return json.dumps(center_object)

    def __str__(self):
        return '{} - {}'.format(self.login, self.id)

    @staticmethod
    def password_match(login, password):
        """
        Check if login matches passworrd
        :param login:
        :param password:
        :return: boolean result flag
        """
        center = Center.query.filter_by(login=login).filter_by(password=password).first()
        if center is None:
            return False
        else:
            return True

    @classmethod
    def get_all_centers(cls):
        """
        :return: centers list
        """
        return [str(center) for center in cls.query.all()]

    @classmethod
    def add_center(cls, address, login, password):
        """
        Add new center
        :param address:
        :param login:
        :param password:
        :return: created center id
        """
        new_center = Center(address, login, password)
        db.session.add(new_center)
        db.session.commit()
        return new_center.id

    @classmethod
    def get_center(cls, center_id):
        """
        Get center by id
        :param center_id:
        :return: center object
        """
        return cls.query.filter_by(id=center_id).first()

    @classmethod
    def get_center_by_name(cls, name):
        """
        Get center by name
        :param name:
        :return: ceenter object
        """
        return cls.query.filter_by(login=name).first()
