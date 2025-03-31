import os
from datetime import timedelta

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    
    # Application configuration
    INVESTMENT_TYPES = ['Equity', 'Debt Fund', 'Liquid Fund', 'Gold', 'Real Estate']
    INVESTMENT_MODES = ['Digital', 'Physical']
    INVESTMENT_GEOGRAPHY = ['India', 'United States']
    RISK_LEVELS = ['High', 'Medium', 'Low']
    LIQUIDITY_LEVELS = ['High', 'Medium', 'Low'] 