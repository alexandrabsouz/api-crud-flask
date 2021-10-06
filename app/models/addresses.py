from app import db

from .paginated import PaginatedAPIMixin


class Address(PaginatedAPIMixin, db.Model):

    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id", ondelete='CASCADE'))
    zip_code = db.Column(db.String(60), index=True)
    state = db.Column(db.String(60))
    city = db.Column(db.String(60))
    number = db.Column(db.String(60))

    def __repr__(self):
        return "<Address: {}>".format(self.id)

    def to_dict(self):
        data = {
            "id": self.id,
            "client_id": self.client_id,
            "zip_code": self.zip_code,
            "state": self.state,
            "city": self.city,
            "number": self.number,
        }
        return data

    def from_dict(self, data):
        for field in ["zip_code", "state", "city", "number"]:
            if field in data:
                setattr(self, field, data[field])
