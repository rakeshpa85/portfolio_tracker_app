from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    portfolio_items = db.relationship('PortfolioItem', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    investment_name = db.Column(db.String(100), nullable=False)
    investment_type = db.Column(db.String(50), nullable=False)
    is_asset = db.Column(db.Boolean, default=True)
    investment_mode = db.Column(db.String(50), nullable=False)
    investment_geography = db.Column(db.String(50), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    liquidity_level = db.Column(db.String(20), nullable=False)
    invested_amount = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'investment_name': self.investment_name,
            'investment_type': self.investment_type,
            'is_asset': self.is_asset,
            'investment_mode': self.investment_mode,
            'investment_geography': self.investment_geography,
            'risk_level': self.risk_level,
            'liquidity_level': self.liquidity_level,
            'invested_amount': self.invested_amount,
            'current_value': self.current_value,
            'value_change': self.value_change,
            'percentage_change': self.percentage_change
        }

    @property
    def value_change(self):
        return self.current_value - self.invested_amount

    @property
    def percentage_change(self):
        if self.invested_amount == 0:
            return 0
        return ((self.current_value - self.invested_amount) / self.invested_amount) * 100

class ConfigurationValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'value': self.value
        } 