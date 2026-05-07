# Daddy - Expense Tracker Application

A modern, full-featured expense tracking application built with Python Flask, SQLite database, and cloud storage integration.

## Features

✅ **User Authentication**
- Secure user registration and login
- Password hashing with werkzeug security

✅ **Expense Management**
- Add, view, edit, and delete expenses
- Organize by categories with custom icons and colors
- Add notes and receipt uploads
- Date and time tracking

✅ **Smart Categories**
- Pre-configured default categories (Food, Transport, Shopping, etc.)
- Create custom categories with emojis
- Color-coded categories for visual organization

✅ **Dashboard & Analytics**
- Real-time expense summary
- Monthly spending overview
- Category breakdown with pie charts
- Daily and weekly trends
- Detailed reports

✅ **Cloud Storage**
- Receipt and document uploads
- Support for Firebase Storage, AWS S3, or local storage
- Easy configuration via environment variables

✅ **Modern UI**
- Responsive Bootstrap 5 design
- Clean and intuitive interface
- Mobile-friendly layout
- Real-time charts and visualizations

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite (upgradeable to PostgreSQL)
- **Frontend**: Bootstrap 5, Chart.js
- **Cloud Storage**: Firebase, AWS S3, or Local Storage
- **Authentication**: Werkzeug Security

## Installation

### 1. Clone the repository
```bash
cd Daddy
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize the database
```bash
python run.py
# In another terminal:
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 6. Run the application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///daddy.db

# Cloud Storage
STORAGE_TYPE=local  # Options: 'local', 'firebase', 's3'

# AWS S3 (if using S3)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET=your-bucket

# Firebase (if using Firebase Storage)
FIREBASE_CREDENTIALS=path/to/credentials.json
```

## Cloud Storage Setup

### Using Firebase Storage

1. Create a Firebase project
2. Download credentials JSON
3. Set `STORAGE_TYPE=firebase` in `.env`
4. Set `FIREBASE_CREDENTIALS` path

### Using AWS S3

1. Create AWS account and S3 bucket
2. Get access keys
3. Set `STORAGE_TYPE=s3` in `.env`
4. Configure AWS credentials

### Using Local Storage

1. Set `STORAGE_TYPE=local` (default)
2. Application stores receipts in `app/static/uploads/`

## Project Structure

```
Daddy/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   ├── routes/               # Route blueprints
│   │   ├── main.py          # Main routes
│   │   ├── auth.py          # Authentication
│   │   ├── expense.py       # Expense management
│   │   └── category.py      # Category management
│   ├── templates/            # HTML templates
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   ├── js/              # JavaScript files
│   │   └── uploads/         # User uploads
│   └── utils/
│       └── cloud_storage.py # Storage integration
├── config/
│   └── config.py            # Configuration classes
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## Usage

### Create Account
1. Go to register page
2. Fill in username, email, and password
3. Account created with default categories

### Add Expense
1. Click "Add Expense" in navigation
2. Fill in details (description, amount, category, date)
3. Optionally upload receipt
4. Click "Add Expense"

### Manage Categories
1. Go to "Categories" section
2. View all categories
3. Add new custom categories with emoji and color
4. Edit or delete categories

### View Reports
1. Go to "Reports" section
2. See monthly spending trends
3. Analyze spending patterns
4. Export data (future feature)

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/logout` - Logout user

### Expenses
- `GET /` - Dashboard
- `GET /expense/add` - Add expense form
- `POST /expense/add` - Create expense
- `GET /expense/edit/<id>` - Edit form
- `POST /expense/edit/<id>` - Update expense
- `GET /expense/delete/<id>` - Delete expense
- `GET /expense/list` - API list expenses

### Categories
- `GET /category/list` - View categories
- `GET /category/add` - Add category form
- `POST /category/add` - Create category
- `GET /category/edit/<id>` - Edit form
- `POST /category/edit/<id>` - Update category
- `GET /category/delete/<id>` - Delete category

## Database Models

### User
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `password` - Hashed password
- `created_at` - Registration timestamp

### Category
- `id` - Primary key
- `name` - Category name
- `icon` - Emoji representation
- `color` - Hex color code
- `user_id` - Foreign key to User

### Expense
- `id` - Primary key
- `description` - Expense description
- `amount` - Expense amount
- `date` - Expense date/time
- `category_id` - Foreign key to Category
- `user_id` - Foreign key to User
- `notes` - Additional notes
- `receipt_url` - Cloud storage URL
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Future Enhancements

- [ ] Recurring expenses
- [ ] Budget alerts and limits
- [ ] Data export (CSV, PDF)
- [ ] Mobile app
- [ ] Multi-currency support
- [ ] Shared expenses / splitting
- [ ] AI-powered expense categorization
- [ ] Advanced analytics and forecasting

## Contributing

Contributions welcome! Please feel free to submit pull requests.

## License

This project is for internal use only.

## Support

For issues or questions, please contact the development team.

---

**Daddy - Track Your Expenses, Master Your Finances** 💰
