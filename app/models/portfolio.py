from app import db
from datetime import datetime

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Investment details
    investment_name = db.Column(db.String(100), nullable=False)
    is_asset = db.Column(db.Boolean, nullable=False)
    investment_type = db.Column(db.String(50), nullable=False)
    investment_mode = db.Column(db.String(20), nullable=False)
    investment_geography = db.Column(db.String(50), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    liquidity_level = db.Column(db.String(20), nullable=False)
    
    # Financial details
    invested_amount = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def value_change(self):
        return self.current_value - self.invested_amount

    @property
    def percentage_change(self):
        if self.invested_amount == 0:
            return 0
        return ((self.current_value - self.invested_amount) / self.invested_amount) * 100

    def __repr__(self):
        return f'<PortfolioItem {self.investment_name}>'

class ConfigurationValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('category', 'value', name='unique_category_value'),
    )

    def __repr__(self):
        return f'<ConfigurationValue {self.category}: {self.value}>' 