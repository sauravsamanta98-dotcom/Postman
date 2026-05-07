"""
Main routes for the application
"""
from flask import render_template, session, redirect, url_for
from datetime import datetime, timedelta
from sqlalchemy import func
from app.routes import main_bp
from app import db
from app.models import Expense, Category, User

def get_currency_symbol(currency_code):
    """Get currency symbol for display"""
    symbols = {
        'INR': '₹',
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'AUD': 'A$',
        'CAD': 'C$',
        'SGD': 'S$'
    }
    return symbols.get(currency_code, currency_code)

@main_bp.route('/')
def index():
    """Home page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Get current month expenses
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    
    expenses = Expense.query.filter_by(user_id=user_id)\
        .filter(Expense.date >= month_start)\
        .order_by(Expense.date.desc())\
        .all()
    
    # Calculate statistics
    total_spent = db.session.query(func.sum(Expense.amount))\
        .filter_by(user_id=user_id)\
        .filter(Expense.date >= month_start)\
        .scalar() or 0
    
    # Category breakdown
    category_stats = db.session.query(
        Category.name,
        Category.icon,
        func.sum(Expense.amount).label('total'),
        func.count(Expense.id).label('count')
    ).join(Expense).filter(
        Expense.user_id == user_id,
        Expense.date >= month_start
    ).group_by(Category.id).all()
    
    # Last 7 days trend
    week_ago = today - timedelta(days=7)
    daily_expenses = db.session.query(
        func.date(Expense.date).label('date'),
        func.sum(Expense.amount).label('total')
    ).filter(
        Expense.user_id == user_id,
        Expense.date >= week_ago
    ).group_by(func.date(Expense.date)).all()
    
    return render_template('dashboard.html',
                         expenses=expenses,
                         total_spent=total_spent,
                         category_stats=category_stats,
                         daily_expenses=daily_expenses)

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.index'))

@main_bp.route('/reports')
def reports():
    """Reports page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Monthly summary
    expenses = Expense.query.filter_by(user_id=user_id).all()
    
    monthly_data = {}
    for expense in expenses:
        month_key = expense.date.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = 0
        monthly_data[month_key] += expense.amount
    
    return render_template('reports.html', monthly_data=monthly_data)
