# Quick Start Guide for Daddy Expense Tracker

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### Option 1: Automatic Setup (Windows)
```bash
setup.bat
```

### Option 2: Automatic Setup (Linux/Mac)
```bash
bash setup.sh
```

### Option 3: Manual Setup

#### 1. Create Virtual Environment
```bash
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` with your settings:
- `FLASK_ENV`: development or production
- `SECRET_KEY`: Change to a secure key
- `STORAGE_TYPE`: local, firebase, or s3
- Database URL for PostgreSQL (optional)

#### 4. Initialize Database
```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

#### 5. Run Application
```bash
python run.py
```

Application will be available at: **http://localhost:5000**

## First Time Usage

1. **Register an Account**
   - Go to http://localhost:5000
   - Click "Register"
   - Create username, email, password
   - Account created with 8 default categories

2. **Add Your First Expense**
   - Click "Add Expense" in navbar
   - Fill in details (description, amount, category, date)
   - Optionally upload a receipt
   - Click "Add Expense"

3. **Manage Categories**
   - Go to "Categories" section
   - Create custom categories with emoji and color
   - Edit or delete as needed

4. **View Dashboard**
   - See monthly spending summary
   - View recent expenses
   - Check spending by category
   - View trends

5. **Generate Reports**
   - Go to "Reports" section
   - View monthly spending charts
   - Analyze spending patterns

## Cloud Storage Setup

### Firebase (Recommended for beginners)
1. Create Firebase project at https://firebase.google.com
2. Download credentials JSON file
3. Add to project and update `.env`:
   ```
   STORAGE_TYPE=firebase
   FIREBASE_CREDENTIALS=/path/to/credentials.json
   ```

### AWS S3
1. Create AWS account and S3 bucket
2. Get access keys from IAM
3. Update `.env`:
   ```
   STORAGE_TYPE=s3
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_S3_BUCKET=your_bucket_name
   AWS_REGION=us-east-1
   ```

### Local Storage (Default)
- No configuration needed
- Receipts stored in `app/static/uploads/`
- Fine for development and internal use

## Default Categories

The app automatically creates these categories:
- 🍔 Food
- 🚗 Transport
- 🛍️ Shopping
- 🎬 Entertainment
- ⚡ Utilities
- ⚕️ Health
- 📚 Education
- 📌 Other

## Troubleshooting

### Port 5000 already in use
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Then kill the process and try again
```

### Database errors
Delete `daddy.db` file and run setup again:
```bash
rm daddy.db
flask shell
>>> from app import db
>>> db.create_all()
```

### Import errors
Make sure virtual environment is activated and all dependencies installed:
```bash
pip install -r requirements.txt
```

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Generate strong `SECRET_KEY`
3. Use PostgreSQL instead of SQLite
4. Set up proper cloud storage (Firebase/S3)
5. Use a production WSGI server (Gunicorn)
6. Set `SESSION_COOKIE_SECURE=True`

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review .env.example for configuration options
3. Check Flask documentation: https://flask.palletsprojects.com/
4. Check Bootstrap documentation: https://getbootstrap.com/

Happy expense tracking! 💰
