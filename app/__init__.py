from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import logging

def create_app():
    """Factory pour créer l'application Flask"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.secret_key = os.environ.get("SESSION_SECRET") or os.urandom(24).hex()
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    logging.basicConfig(level=logging.DEBUG)
    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = None
    app.config['SESSION_COOKIE_NAME'] = 'admin_session'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400
    
    from app.database import init_db
    init_db(app)
    
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.superadmin import superadmin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(superadmin_bp)
    
    return app
