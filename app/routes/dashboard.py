from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models import PortfolioItem
from app import db
from sqlalchemy import func
from datetime import datetime

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')

@bp.route('/api/chart-data')
@login_required
def chart_data():
    # Get filter parameter
    show_assets_only = request.args.get('assets_only', 'true').lower() == 'true'
    
    # Base query
    query = PortfolioItem.query.filter_by(user_id=current_user.id)
    if show_assets_only:
        query = query.filter_by(is_asset=True)
    
    items = query.all()
    
    # Prepare data for investment type distribution
    investment_types = {}
    total_current_value = 0
    
    for item in items:
        if item.investment_type not in investment_types:
            investment_types[item.investment_type] = {
                'invested_amount': 0,
                'current_value': 0
            }
        investment_types[item.investment_type]['invested_amount'] += item.invested_amount
        investment_types[item.investment_type]['current_value'] += item.current_value
        total_current_value += item.current_value
    
    # Prepare summary table data
    summary_data = []
    for inv_type, values in investment_types.items():
        percentage = (values['current_value'] / total_current_value * 100) if total_current_value > 0 else 0
        summary_data.append({
            'investment_type': inv_type,
            'invested_amount': values['invested_amount'],
            'current_value': values['current_value'],
            'percentage': percentage
        })
    
    # Add total row
    total_invested = sum(item['invested_amount'] for item in summary_data)
    summary_data.append({
        'investment_type': 'Total',
        'invested_amount': total_invested,
        'current_value': total_current_value,
        'percentage': 100
    })
    
    # Prepare monthly data for bar and trend charts
    monthly_data = {}
    for item in items:
        # Use the current month-year as we don't have historical data
        month_year = datetime.now().strftime('%b%Y')
        
        if month_year not in monthly_data:
            monthly_data[month_year] = {}
        
        if item.investment_type not in monthly_data[month_year]:
            monthly_data[month_year][item.investment_type] = {
                'invested_amount': 0,
                'current_value': 0
            }
        
        monthly_data[month_year][item.investment_type]['invested_amount'] += item.invested_amount
        monthly_data[month_year][item.investment_type]['current_value'] += item.current_value
    
    # Convert monthly data to format suitable for charts
    chart_data = []
    for month_year, type_data in monthly_data.items():
        for inv_type, values in type_data.items():
            chart_data.append({
                'month_year': month_year,
                'investment_type': inv_type,
                'invested_amount': values['invested_amount'],
                'current_value': values['current_value']
            })
    
    return jsonify({
        'value_distribution': {
            'labels': list(investment_types.keys()),
            'values': [data['current_value'] for data in investment_types.values()]
        },
        'percentage_distribution': {
            'labels': list(investment_types.keys()),
            'values': [(data['current_value'] / total_current_value * 100) if total_current_value > 0 else 0 
                      for data in investment_types.values()]
        },
        'summary_data': summary_data,
        'monthly_data': chart_data
    }) 