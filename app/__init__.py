from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)
login_manager= LoginManager(app)

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    from app import routes
    from app import auth

    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth.auth_bp)

    #db.create_all()
