import base64
import os
from datetime import datetime, timedelta

from app import db
from sqlalchemy.orm import backref
from werkzeug.security import check_password_hash, generate_password_hash

from .paginated import PaginatedAPIMixin
from .addresses import Address


class Client(PaginatedAPIMixin, db.Model):

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))
    address = db.relationship("Address", backref=backref("client", passive_deletes=True))
    product = db.relationship("Product", backref=backref("client", passive_deletes=True))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Client.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self):
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email
        }
        return data

    def to_dict_with_address(self):
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": {
                "zip_code": self.address.zip_code,
                "city": self.address.city,
                "state": self.address.state,
                "number": self.address.number
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ["email", "full_name"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])

    def __repr__(self):
        return "<Clients: {}>".format(self.id)


