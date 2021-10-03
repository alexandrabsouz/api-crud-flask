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

