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


@api.route('/clients/<int:id>', methods=['GET'])
@token_auth.login_required
def get_client(id):
    return jsonify(Client.query.get_or_404(id).to_dict())


@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    if 'zip_code' not in data['address'] or 'state' not in data['address'] or 'city' not in data['address'] or 'number' not in data['address']:
        return bad_request('Must include zip_code, state, city and number')
    if 'email' not in data or 'full_name' not in data or 'password' not in data:
        return bad_request('Must include full_name, email and password')
    if Client.query.filter_by(email=data['email']).first():
        return bad_request('Please use another e-mail')
    client = Client()
    client.from_dict(data, new_user=True)
    db.session.add(client)
    db.session.commit()
    address = Address(client_id=client.id, zip_code=data['address']['zip_code'], state=data['address']['state'], city=data['address']['city'], number=data['address']['number'])
    db.session.add(address)
    db.session.commit()
    response = jsonify(client.to_dict_with_address())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_client', id=client.id)
    return response
