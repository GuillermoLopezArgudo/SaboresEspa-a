from app.routes.auth import auth_bp
from app.routes.health import health_bp
from app.routes.media import media_bp
from app.routes.recipes import recipes_bp
from app.routes.users import users_bp


def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(media_bp)
