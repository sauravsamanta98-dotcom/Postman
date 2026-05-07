"""
Daddy - Expense Tracker Application
Entry point for running the Flask application
"""
import os
from app import create_app, db
from app.models import Expense, Category, User

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Expense': Expense, 'Category': Category, 'User': User}

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
