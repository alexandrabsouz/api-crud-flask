from app import db

from .paginated import PaginatedAPIMixin


class Product(PaginatedAPIMixin, db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id", ondelete='CASCADE'))
    name = db.Column(db.String(60))
    price = db.Column(db.Float)
    description = db.Column(db.String(300))
    img_url = db.Column(db.String(300))

    def __repr__(self):
        return "<Product: {}>".format(self.id)

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "img_url": self.img_url
        }
        return data

    def from_dict(self, data):
        for field in ["name", "price", "description", "img_url"]:
            if field in data:
                setattr(self, field, data[field])
