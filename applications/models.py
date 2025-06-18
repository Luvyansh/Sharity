from applications.database import db
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    
    roles = db.relationship('Role', secondary='user_roles')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class StockCache(db.Model):
    __tablename__ = 'stock_cache'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    currency = db.Column(db.String(10))  # ✅ Define the field here
    market_cap = db.Column(db.BigInteger)
    sector = db.Column(db.String(100))
    last_updated = db.Column(db.DateTime)

class NewsCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String, unique=True, nullable=False)
    articles = db.Column(JSON)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)