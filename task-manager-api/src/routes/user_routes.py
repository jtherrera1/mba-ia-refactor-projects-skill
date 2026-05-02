from flask import Blueprint, request, jsonify
from src.controllers.user_controller import (
    list_users, get_user, create_user, update_user,
    delete_user, get_user_tasks, login,
)

user_bp = Blueprint('users', __name__)


@user_bp.route('/users', methods=['GET'])
def index():
    data, status = list_users()
    return jsonify(data), status


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def show(user_id):
    data, status = get_user(user_id)
    return jsonify(data), status


@user_bp.route('/users', methods=['POST'])
def create():
    data, status = create_user(request.get_json())
    return jsonify(data), status


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update(user_id):
    data, status = update_user(user_id, request.get_json())
    return jsonify(data), status


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    data, status = delete_user(user_id)
    return jsonify(data), status


@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def user_tasks(user_id):
    data, status = get_user_tasks(user_id)
    return jsonify(data), status


@user_bp.route('/login', methods=['POST'])
def do_login():
    data, status = login(request.get_json())
    return jsonify(data), status
