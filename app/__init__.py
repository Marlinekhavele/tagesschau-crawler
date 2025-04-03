from flask import Flask
from flask_migrate import Migrate
from app.database.db import db
from app.routes.article import register_routes
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    register_routes(app)
    
    with app.app_context():
        db.create_all()
    
    return app