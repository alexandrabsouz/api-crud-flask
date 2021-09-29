from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from app import db
import os
import base64



class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            "items": [item.to_dict() for item in resources.items],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total,
            },
            "_links": {
                "self": url_for(endpoint, page=page, per_page=per_page, **kwargs),
                "next": url_for(endpoint, page=page + 1, per_page=per_page, **kwargs)
                if resources.has_next
                else None,
                "prev": url_for(endpoint, page=page - 1, per_page=per_page, **kwargs)
                if resources.has_prev
                else None,
            },
        }
        return data


class Client(PaginatedAPIMixin, db.Model):

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))
    address = db.relationship("Address", backref="client", uselist=False)
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


class Address(PaginatedAPIMixin, db.Model):

    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
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
