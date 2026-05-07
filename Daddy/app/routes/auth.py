"""
Authentication routes
"""
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import auth_bp
from app import db
from app.models import User, Category

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        # Create default categories
        default_categories = [
            {'name': 'Food', 'icon': '🍔', 'color': '#e74c3c'},
            {'name': 'Transport', 'icon': '🚗', 'color': '#3498db'},
            {'name': 'Shopping', 'icon': '🛍️', 'color': '#9b59b6'},
            {'name': 'Entertainment', 'icon': '🎬', 'color': '#f39c12'},
            {'name': 'Utilities', 'icon': '⚡', 'color': '#1abc9c'},
            {'name': 'Health', 'icon': '⚕️', 'color': '#c0392b'},
            {'name': 'Education', 'icon': '📚', 'color': '#2980b9'},
            {'name': 'Other', 'icon': '📌', 'color': '#95a5a6'},
        ]
        
        for cat in default_categories:
            category = Category(**cat, user_id=user.id)
            db.session.add(category)
        
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password functionality"""
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        user = User.query.filter_by(email=email, username=username).first()
        
        if not user:
            flash('Email or username not found', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        # Update password
        user.password = generate_password_hash(new_password)
        db.session.commit()
        
        flash('Password reset successfully! Please login with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('forgot_password.html')

@auth_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """User settings"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        currency = request.form.get('currency', 'INR')
        user.currency = currency
        db.session.commit()
        flash(f'Currency changed to {currency}!', 'success')
        return redirect(url_for('auth.settings'))
    
    currencies = {
        'INR': '₹ Indian Rupee',
        'USD': '$ US Dollar',
        'EUR': '€ Euro',
        'GBP': '£ British Pound',
        'JPY': '¥ Japanese Yen',
        'AUD': 'A$ Australian Dollar',
        'CAD': 'C$ Canadian Dollar',
        'SGD': 'S$ Singapore Dollar'
    }
    
    return render_template('settings.html', user=user, currencies=currencies)
