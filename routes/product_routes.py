from flask import Blueprint, jsonify
from controllers.product_controller import get_products

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products', methods=['GET'])
def list_products():
    products = get_products()
    return jsonify({
        "success": True,
        "data": products
    })