import os
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from config.config import get_config_by_name
from db.db import db
from models.user import User
from modules.user import user_bp
from modules.home import home_bp
from modules.device import device_bp
from modules.admin import admin_bp

load_dotenv()

config=os.getenv('FLASK_ENV') or 'development'

app = Flask(__name__)
app.config.from_object(get_config_by_name(config))

with app.app_context():
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()

with app.app_context():
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(device_bp, url_prefix='/device')
    app.register_blueprint(admin_bp, url_prefix='/admin')

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

jwt = JWTManager(app)

@jwt.unauthorized_loader
def my_invalid_token_callback(expired_token):
    return make_response(jsonify(message='Missing Authorization Header'), 401)

if __name__ == "__main__":
    if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5000, app)