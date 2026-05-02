from flask import Blueprint, request, jsonify
from src.controllers.task_controller import (
    list_tasks, get_task, create_task, update_task,
    delete_task, search_tasks, get_task_stats,
)

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['GET'])
def index():
    data, status = list_tasks()
    return jsonify(data), status


@task_bp.route('/tasks/search', methods=['GET'])
def search():
    data, status = search_tasks(
        query=request.args.get('q', ''),
        status=request.args.get('status', ''),
        priority=request.args.get('priority', ''),
        user_id=request.args.get('user_id', ''),
    )
    return jsonify(data), status


@task_bp.route('/tasks/stats', methods=['GET'])
def stats():
    data, status = get_task_stats()
    return jsonify(data), status


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def show(task_id):
    data, status = get_task(task_id)
    return jsonify(data), status


@task_bp.route('/tasks', methods=['POST'])
def create():
    data, status = create_task(request.get_json())
    return jsonify(data), status


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update(task_id):
    data, status = update_task(task_id, request.get_json())
    return jsonify(data), status


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    data, status = delete_task(task_id)
    return jsonify(data), status
