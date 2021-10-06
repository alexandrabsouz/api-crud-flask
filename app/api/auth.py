from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import Client
from app.api.errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = Client.query.filter_by(email=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.verify_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = Client.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)
