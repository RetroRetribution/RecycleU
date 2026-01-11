from flask import Flask
import os
from jinja2 import TemplateNotFound, TemplateSyntaxError
from .db import init_db
from .routes.pages import pages_bp
from .routes.auth import auth_bp

def create_app():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_folder = os.path.join(BASE_DIR, 'templates')
    static_folder = os.path.join(BASE_DIR, 'static')

    # Use the computed absolute folders (was using literal strings)
    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder,
        static_url_path='/static'
    )
    app.secret_key = 'your-secret-key-here'

    # Helpful during development
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True

    # Log resolved folders to help diagnose missing-template issues
    app.logger.debug("Template folder: %s", app.template_folder)
    app.logger.debug("Static folder: %s", app.static_folder)

    init_db(app)

    # Always register core blueprints
    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)

    # Conditionally register optional blueprints if they exist
    try:
        from .routes.api_user import user_api_bp
        app.register_blueprint(user_api_bp)
    except ImportError:
        pass

    try:
        from .routes.api_rewards import rewards_api_bp
        app.register_blueprint(rewards_api_bp)
    except ImportError:
        pass

    # Better error messages for template problems
    @app.errorhandler(TemplateNotFound)
    def _handle_template_not_found(err):
        app.logger.error("Template not found: %s", getattr(err, 'name', str(err)))
        return f"Template not found: {getattr(err, 'name', str(err))}", 500

    @app.errorhandler(TemplateSyntaxError)
    def _handle_template_syntax_error(err):
        msg = f"{getattr(err, 'filename', '')}: {getattr(err, 'message', str(err))}"
        app.logger.error("Template syntax error: %s", msg)
        return f"Template syntax error: {msg}", 500

    return app