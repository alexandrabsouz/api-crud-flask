from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Product
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/products', methods=['GET'])
@token_auth.login_required
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_products')
    return jsonify(data)


@api.route('/products/<int:id>', methods=['GET'])
@token_auth.login_required
def get_product(id):
    return jsonify(Product.query.get_or_404(id).to_dict())


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