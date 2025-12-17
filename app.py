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

    @app.route('/user', methods=['POST'])
    def create_user():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            return jsonify({"error": "User with this username or email already exists"}), 409
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    
    @app.route('/get_user/<int:user_id>', methods=['GET'])
    @login_required
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user": user.username}), 200

    @app.route('/update_user/<int:user_id>', methods=['PUT'])
    @login_required
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        data = request.get_json()
        password = data.get('password')

        if password:
            user.password = password
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200

    @app.route('/delete_user/<int:user_id>', methods=['DELETE'])
    @login_required
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if current_user == user:
            return jsonify({"error": "You are not authorized to delete this user"}), 403
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=EnviorementConfig.HOST, port=EnviorementConfig.PORT, debug=EnviorementConfig.DEBUG)