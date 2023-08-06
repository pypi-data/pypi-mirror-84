from sitepipes import db


class Device(db.Model):
    """ A smart device that generates data """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)


class Provider(db.Model):
    """ A healthcare provider with medical records """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)
