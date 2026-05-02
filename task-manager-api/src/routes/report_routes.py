from flask import Blueprint, request, jsonify
from src.controllers.report_controller import summary_report, user_report
from src.controllers.category_controller import (
    list_categories, create_category, update_category, delete_category,
)

report_bp = Blueprint('reports', __name__)


@report_bp.route('/reports/summary', methods=['GET'])
def summary():
    data, status = summary_report()
    return jsonify(data), status


@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user(user_id):
    data, status = user_report(user_id)
    return jsonify(data), status


@report_bp.route('/categories', methods=['GET'])
def categories_index():
    data, status = list_categories()
    return jsonify(data), status


@report_bp.route('/categories', methods=['POST'])
def categories_create():
    data, status = create_category(request.get_json())
    return jsonify(data), status


@report_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def categories_update(cat_id):
    data, status = update_category(cat_id, request.get_json())
    return jsonify(data), status


@report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def categories_delete(cat_id):
    data, status = delete_category(cat_id)
    return jsonify(data), status
