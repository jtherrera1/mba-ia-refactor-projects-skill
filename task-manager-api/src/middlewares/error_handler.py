import logging
from flask import jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(exc):
        return jsonify({'error': 'Bad request', 'message': str(exc)}), 400

    @app.errorhandler(404)
    def not_found(exc):
        return jsonify({'error': 'Not found', 'message': str(exc)}), 404

    @app.errorhandler(405)
    def method_not_allowed(exc):
        return jsonify({'error': 'Method not allowed'}), 405

    @app.errorhandler(500)
    def internal_error(exc):
        logger.error('Unhandled server error: %s', exc)
        return jsonify({'error': 'Internal server error'}), 500
