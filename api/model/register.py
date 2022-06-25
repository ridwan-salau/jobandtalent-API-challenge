from api import db


class RegisterModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_data = db.Column(db.String(1000), unique=True, nullable=False)
    dev1 = db.Column(db.String(20), nullable=False)
    dev2 = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Register %r>' % self.dev1 + self.dev2
