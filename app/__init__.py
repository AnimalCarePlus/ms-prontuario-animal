from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .models import db
from .routes import api
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)

    
    swagger = Swagger(app, template_file='docs/swagger.yaml')

    app.register_blueprint(api, url_prefix='/api')

    with app.app_context():
        import os
        if not os.path.exists('prontuario.db'):
            db.create_all()
            print("Banco de dados criado!")

    return app
