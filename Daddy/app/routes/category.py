"""
Category management routes
"""
from flask import render_template, request, redirect, url_for, session, flash
from app.routes import category_bp
from app import db
from app.models import Category

@category_bp.route('/list')
def list_categories():
    """List all categories"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    categories = Category.query.filter_by(user_id=user_id, active_status='A').all()
    
    return render_template('categories.html', categories=categories)

@category_bp.route('/add', methods=['GET', 'POST'])
def add_category():
    """Add a new category"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    if request.method == 'POST':
        name = request.form.get('name')
        icon = request.form.get('icon', '📁')
        color = request.form.get('color', '#3498db')
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('category.add_category'))
        
        if Category.query.filter_by(name=name, user_id=user_id, active_status='A').first():
            flash('Category already exists', 'error')
            return redirect(url_for('category.add_category'))
        
        category = Category(name=name, icon=icon, color=color, user_id=user_id)
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('category.list_categories'))
    
    return render_template('add_category.html')

@category_bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """Edit a category"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    category = Category.query.filter_by(id=category_id, user_id=user_id, active_status='A').first()
    
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('category.list_categories'))
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.icon = request.form.get('icon')
        category.color = request.form.get('color')
        
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('category.list_categories'))
    
    return render_template('edit_category.html', category=category)

@category_bp.route('/delete/<int:category_id>')
def delete_category(category_id):
    """Delete a category (soft delete)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    category = Category.query.filter_by(id=category_id, user_id=user_id, active_status='A').first()
    
    if category:
        category.active_status = 'D'  # Mark as deleted
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    else:
        flash('Category not found', 'error')
    
    return redirect(url_for('category.list_categories'))
