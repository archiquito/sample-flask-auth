from flask import Flask, jsonify
from flask_cors import CORS
from db import db
from config import EnviorementConfig

def create_app(config_class=EnviorementConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.SQLALCHEMY_DATABASE_URI
    CORS(app)
    db.init_app(app)
    
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Flask App!"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=EnviorementConfig.HOST, port=EnviorementConfig.PORT, debug=EnviorementConfig.DEBUG)