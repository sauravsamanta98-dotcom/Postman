"""
Routes package
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
expense_bp = Blueprint('expense', __name__)
category_bp = Blueprint('category', __name__)

from app.routes import main, auth, expense, category
