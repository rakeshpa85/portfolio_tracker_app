from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from app import db
from app.models import ConfigurationValue

bp = Blueprint('config', __name__, url_prefix='/config')

@bp.route('/')
@login_required
def index():
    # Define available categories
    categories = {
        'investment_type': 'Investment Types',
        'investment_mode': 'Investment Modes',
        'investment_geography': 'Investment Geography',
        'risk_level': 'Risk Levels',
        'liquidity_level': 'Liquidity Levels'
    }
    
    # Get all configuration values grouped by category
    config_values = {}
    for category_key in categories.keys():
        config_values[category_key] = ConfigurationValue.query.filter_by(category=category_key).all()
    
    return render_template('config/index.html', categories=categories, config_values=config_values)

@bp.route('/add', methods=['POST'])
@login_required
def add_value():
    try:
        category = request.form['category']
        value = request.form['value']
        
        # Check if value already exists in this category
        if ConfigurationValue.query.filter_by(category=category, value=value).first():
            flash('This value already exists in the selected category.', 'error')
            return redirect(url_for('config.index'))
        
        config_value = ConfigurationValue(category=category, value=value)
        db.session.add(config_value)
        db.session.commit()
        flash('Configuration value added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding configuration value: {str(e)}', 'error')
    return redirect(url_for('config.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_value(id):
    try:
        config_value = ConfigurationValue.query.get_or_404(id)
        db.session.delete(config_value)
        db.session.commit()
        flash('Configuration value deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting configuration value: {str(e)}', 'error')
    return redirect(url_for('config.index'))

@bp.route('/api/values/<category>')
@login_required
def get_values(category):
    values = [config.value for config in ConfigurationValue.query.filter_by(category=category).all()]
    return jsonify(values) 