import logging
import datetime
from flask import Flask
from flask_cors import CORS
from src.config import settings
from src.config.database import db
from src.routes.task_routes import task_bp
from src.routes.user_routes import user_bp
from src.routes.report_routes import report_bp
from src.middlewares.error_handler import register_error_handlers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = settings.SECRET_KEY

    CORS(app)
    db.init_app(app)

    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)

    register_error_handlers(app)

    @app.route('/health')
    def health():
        return {'status': 'ok', 'timestamp': str(datetime.datetime.now())}

    @app.route('/')
    def index():
        return {'message': 'Task Manager API', 'version': '2.0'}

    with app.app_context():
        import src.models  # noqa: F401 — registers all models with SQLAlchemy
        db.create_all()

    return app
