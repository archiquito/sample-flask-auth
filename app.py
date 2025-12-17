from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db
from config import EnviorementConfig
from models.user import User
from login import login_manager, login_user, check_password_hash, current_user, logout_user, login_required

def create_app(config_class=EnviorementConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = config_class.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.SQLALCHEMY_DATABASE_URI
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    #login view
    login_manager.login_view = 'login'
    #session protection
    login_manager.session_protection = 'strong'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Flask App!"})
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            return jsonify({"error": "Invalid username or password"}), 401

        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    
    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=EnviorementConfig.HOST, port=EnviorementConfig.PORT, debug=EnviorementConfig.DEBUG)