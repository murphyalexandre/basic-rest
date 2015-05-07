from datetime import datetime

from app import db


class Car(db.Model):
    """
    A car object.
    """
    __table_name__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    cylinders = db.Column(db.Integer)
    make = db.Column(db.String(255))
    model = db.Column(db.String(255))
    year = db.Column(db.Integer)
    owner = db.Column(db.String(255))
    image = db.Column(db.String(512))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
           'id': self.id,
           'description': self.description,
           'cylinders': self.cylinders,
           'make': self.make,
           'model': self.model,
           'year': self.year,
           'owner': self.owner,
           'image': self.image,
           'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return '<Car {} {} {} {}>'.format(
                                self.owner, self.make, self.model, self.year)
