from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Product
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIRECTORY = os.path.join(BASE_DIR, "uploads/")

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@api.route('/products/<int:id>', methods=['GET'])
@token_auth.login_required
def get_product(id):
    return jsonify(Product.query.get_or_404(id).to_dict())


@api.route('/products', methods=['GET'])
@token_auth.login_required
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_products')
    return jsonify(data)


@api.route('/product', methods=['POST'])
@token_auth.login_required
def create_product():
    data = request.get_json() or {}
    if 'name' not in data or 'price' not in data or 'description' not in data or 'img_url' not in data:
        return bad_request('Must include name, price, description, img_url')
    product = Product()
    product.from_dict(data)
    product.client_id = g.current_user.id
    db.session.add(product)
    db.session.commit()
    response = jsonify(product.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_product', id=product.id)
    return response


@api.route('/product/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_product(id):
    if g.current_user.id != id:
        abort(403)
    product = Product.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' not in data or 'price' not in data or 'description' not in data or 'img_url' not in data:
        return bad_request('price, description, name or img_url missing')
    product.from_dict(data)
    db.session.commit()
    return jsonify(product.to_dict())


@api.route('/product/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "resource deleted"}), 202