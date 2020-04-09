from app import db


class Access(db.Model):
    """
    API access nodel class
    """
    __tablename__ = 'audit'
    center_id = db.Column(db.Integer, db.ForeignKey('centers.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, primary_key=True)

    def __init__(self, center_id, timestamp):
        self.center_id = center_id
        self.timestamp = timestamp

    @classmethod
    def add_access_entry(cls, center_id, timestamp):
        """
        Add new access entry
        :param center_id:
        :param timestamp:
        :return:
        """
        new_access_entry = cls(center_id, timestamp)
        db.session.add(new_access_entry)
        db.session.commit()
