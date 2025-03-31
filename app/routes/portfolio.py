from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import PortfolioItem

bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@bp.route('/')
@login_required
def index():
    portfolio_items = PortfolioItem.query.filter_by(user_id=current_user.id).all()
    return render_template('portfolio/index.html', portfolio_items=portfolio_items)

@bp.route('/add', methods=['POST'])
@login_required
def add_investment():
    try:
        data = request.form
        investment = PortfolioItem(
            user_id=current_user.id,
            investment_name=data['investment_name'],
            investment_type=data['investment_type'],
            is_asset=data.get('is_asset') == 'Asset',
            investment_mode=data['investment_mode'],
            investment_geography=data['investment_geography'],
            risk_level=data['risk_level'],
            liquidity_level=data['liquidity_level'],
            invested_amount=float(data['invested_amount']),
            current_value=float(data['current_value'])
        )
        db.session.add(investment)
        db.session.commit()
        flash('Investment added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding investment: {str(e)}', 'error')
    return redirect(url_for('portfolio.index'))

@bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_investment(id):
    try:
        investment = PortfolioItem.query.get_or_404(id)
        if investment.user_id != current_user.id:
            flash('You do not have permission to edit this investment.', 'error')
            return redirect(url_for('portfolio.index'))

        data = request.form
        investment.investment_name = data['investment_name']
        investment.investment_type = data['investment_type']
        investment.is_asset = data.get('is_asset') == 'Asset'
        investment.investment_mode = data['investment_mode']
        investment.investment_geography = data['investment_geography']
        investment.risk_level = data['risk_level']
        investment.liquidity_level = data['liquidity_level']
        investment.invested_amount = float(data['invested_amount'])
        investment.current_value = float(data['current_value'])

        db.session.commit()
        flash('Investment updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating investment: {str(e)}', 'error')
    return redirect(url_for('portfolio.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        investment = PortfolioItem.query.get_or_404(id)
        if investment.user_id != current_user.id:
            flash('You do not have permission to delete this investment.', 'error')
            return redirect(url_for('portfolio.index'))

        db.session.delete(investment)
        db.session.commit()
        flash('Investment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting investment: {str(e)}', 'error')
    return redirect(url_for('portfolio.index'))

@bp.route('/api/calculate', methods=['POST'])
@login_required
def calculate_changes():
    try:
        data = request.get_json()
        invested_amount = float(data['invested_amount'])
        current_value = float(data['current_value'])
        
        value_change = current_value - invested_amount
        percentage_change = ((current_value - invested_amount) / invested_amount * 100) if invested_amount != 0 else 0
        
        return jsonify({
            'value_change': value_change,
            'percentage_change': percentage_change
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400 