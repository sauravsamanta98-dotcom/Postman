"""
Expense management routes
"""
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from app.routes import expense_bp
from app import db
from app.models import Expense, Category, User
from app.utils.cloud_storage import upload_receipt

@expense_bp.route('/add', methods=['GET', 'POST'])
def add_expense():
    """Add a new expense"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    categories = Category.query.filter_by(user_id=user_id, active_status='A').all()
    
    if request.method == 'POST':
        description = request.form.get('description')
        amount = request.form.get('amount')
        category_id = request.form.get('category_id')
        date_str = request.form.get('date')
        notes = request.form.get('notes')
        
        if not all([description, amount, category_id]):
            flash('All required fields must be filled', 'error')
            return redirect(url_for('expense.add_expense'))
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except ValueError:
            flash('Invalid amount', 'error')
            return redirect(url_for('expense.add_expense'))
        
        # Verify category belongs to user
        category = Category.query.filter_by(id=category_id, user_id=user_id).first()
        if not category:
            flash('Invalid category', 'error')
            return redirect(url_for('expense.add_expense'))
        
        expense_date = datetime.fromisoformat(date_str) if date_str else datetime.utcnow()
        
        # Handle file upload (receipt)
        receipt_url = None
        if 'receipt' in request.files:
            file = request.files['receipt']
            if file.filename != '':
                receipt_url = upload_receipt(file, user_id)
        
        expense = Expense(
            description=description,
            amount=amount,
            category_id=category_id,
            user_id=user_id,
            date=expense_date,
            notes=notes,
            receipt_url=receipt_url
        )
        
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_expense.html', categories=categories)

@expense_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """Edit an expense"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id, active_status='A').first()
    
    if not expense:
        flash('Expense not found', 'error')
        return redirect(url_for('main.index'))
    
    categories = Category.query.filter_by(user_id=user_id, active_status='A').all()
    
    if request.method == 'POST':
        expense.description = request.form.get('description')
        expense.amount = float(request.form.get('amount'))
        expense.category_id = request.form.get('category_id')
        expense.notes = request.form.get('notes')
        
        if 'receipt' in request.files:
            file = request.files['receipt']
            if file.filename != '':
                receipt_url = upload_receipt(file, user_id)
                expense.receipt_url = receipt_url
        
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('edit_expense.html', expense=expense, categories=categories)

@expense_bp.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    """Delete an expense (soft delete)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id, active_status='A').first()
    
    if expense:
        expense.active_status = 'D'  # Mark as deleted
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Expense not found', 'error')
    
    return redirect(url_for('main.index'))

@expense_bp.route('/list')
def list_expenses():
    """API endpoint to list expenses"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).all()
    
    return jsonify([expense.to_dict() for expense in expenses])
