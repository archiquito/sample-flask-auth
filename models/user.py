from db import db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'