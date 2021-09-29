from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Client, Address
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/clients', methods=['GET'])
@token_auth.login_required
def get_clients():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Client.to_collection_dict(Client.query, page, per_page, 'api.get_clients')
    return jsonify(data)