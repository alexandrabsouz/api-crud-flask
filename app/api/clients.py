from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Client, Address, Product
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route("/client/products/<int:client_id>", methods=['GET'])
@token_auth.login_required
def list_all_products_from_id(client_id):
    query = Product.query.filter_by(client_id=client_id).all()
    products = [product.to_dict() for product in query]
    return jsonify(products)


@api.route('/client/<int:id>', methods=['GET'])
@token_auth.login_required
def get_client(id):
    return jsonify(Client.query.get_or_404(id).to_dict())


@api.route('/clients', methods=['GET'])
@token_auth.login_required
def get_clients():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Client.to_collection_dict(Client.query, page, per_page, 'api.get_clients')
    return jsonify(data)


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


@api.route('/client/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_client(id):
    if g.current_user.id != id:
        abort(403)
    client = Client.query.get_or_404(id)
    data = request.get_json() or {}
    if 'full_name' not in data:
        return bad_request('full_name is missing')
    elif 'email' in data and data['email'] != client.email and \
            Client.query.filter_by(email=data['email']).first():
        return bad_request('Use another email')
    client.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(Client.to_dict())


@api.route('/client/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "resource deleted"}), 202
