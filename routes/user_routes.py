from flask import Blueprint, jsonify, request
from controllers.user_controller import get_users, create_user, update_user, delete_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def list_users():
    users = get_users()
    return jsonify({
        "success": True,
        "data": users
    })

@user_routes.route('/users', methods=['POST'])
def add_user():
    user_data = request.get_json()
    new_user, error = create_user(user_data)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), 400

        
    return jsonify({
        "success": True,
        "message": "User created successfully.",
        "data": new_user
    }), 201

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    user_data = request.get_json()
    updated_user, error = update_user(user_id, user_data)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), 404

    return jsonify({
        "success": True,
        "message": "User updated successfully.",
        "data": updated_user
    })

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    success, error = delete_user(user_id)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), 404

    return jsonify({
        "success": True,
        "message": "User deleted successfully."
    })