#  Spendly - Personal Budget Tracker

A full-stack personal budget tracking application built with Django REST Framework and React. Track your income, expenses, set budgets, and visualize your financial data with interactive D3.js charts.

##  Project Overview

Spendly helps users manage their personal finances by:
- Tracking income and expenses with detailed categorization
- Setting and monitoring monthly budgets
- Visualizing financial data with interactive charts
- Filtering and analyzing transaction history

##  Tech Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Authentication**: Token-based authentication
- **Additional Libraries**:
  - django-cors-headers 4.3.1
  - django-filter 23.5

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Routing**: React Router DOM 6.20.0
- **HTTP Client**: Axios 1.6.2
- **Data Visualization**: D3.js 7.8.5

##  Features

### Authentication
- Secure token-based authentication
- User registration (sign-up) with auto-login
- Protected routes and API endpoints
- User session management
- Automatic default categories for new users

### Transaction Management
- Add, edit, and delete income/expense transactions
- Categorize transactions
- Add descriptions and dates
- Full CRUD operations

### Transaction Overview
- Paginated transaction list
- Advanced filtering by:
  - Date range
  - Category
  - Amount range
  - Transaction type (income/expense)
- Sort by date or amount
- Responsive table design

### Budget Management
- Set monthly budgets (overall or per-category)
- Real-time budget tracking
- Visual progress indicators
- Budget vs. actual expense comparison
- D3.js bar chart visualization

### Dashboard
- Financial summary (total income, expenses, balance)
- D3.js pie chart showing expense breakdown by category
- Category-wise income and expense summaries
- Recent transactions overview

##  Prerequisites

- Python 3.8 or higher (accessible via `py` or `python` command)
- Node.js 16.x or higher
- npm or yarn package manager

> **Note:** Virtual environment is optional. You can run directly with `py` command.

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Install dependencies**
```bash
# Using py command (Windows)
py -m pip install -r requirements.txt

# OR using python directly
pip install -r requirements.txt
```

> **Note:** Virtual environment is optional but recommended for isolation. If you want to use venv:
> ```bash
> py -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> ```

3. **Run migrations**
```bash
# Using py command
py manage.py makemigrations
py manage.py migrate

# OR using python
python manage.py migrate
```

4. **Create superuser (optional, for admin access)**
```bash
py manage.py createsuperuser
```

5. **Set up demo data**
```bash
py setup_initial_data.py
```

This script creates:
- Demo user account
- Sample income and expense categories
- Sample transactions for the last 3 months
- Sample monthly budget

6. **Run development server**
```bash
py manage.py runserver
```

The backend API will be available at: `http://localhost:8000/api/`
Django admin panel: `http://localhost:8000/admin/`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create environment file**
```bash
# Create .env file
cp .env.example .env
```

Edit `.env` and set:
```
VITE_API_URL=http://localhost:8000/api
```

4. **Run development server**
```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173/`

##  Access the Application

### Option 1: Create Your Own Account
1. Go to http://localhost:5173/register
2. Fill in the registration form (minimum 8 character password)
3. You'll be automatically logged in with default categories created

### Option 2: Use Test Account
**Username**: `demo`  
**Password**: `demo123456`

##  API Documentation

The Django REST Framework provides a browsable API interface.

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user (returns token)
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout and invalidate token
- `GET /api/auth/user/` - Get current user information

### Categories Endpoints
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Transactions Endpoints
- `GET /api/transactions/` - List transactions (paginated)
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/{id}/` - Get transaction details
- `PUT /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `GET /api/transactions/summary/` - Get financial summary

#### Transaction Filters
- `?type=income` or `?type=expense`
- `?category={category_id}`
- `?date_from=2024-01-01`
- `?date_to=2024-12-31`
- `?amount_min=100`
- `?amount_max=1000`

### Budget Endpoints
- `GET /api/budgets/` - List budgets
- `POST /api/budgets/` - Create budget
- `GET /api/budgets/{id}/` - Get budget details
- `PUT /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget
- `GET /api/budgets/current_month/` - Get current month budgets

##  Features Implemented

### Required Features ✅
- [x] User authentication with Django REST Framework
- [x] Protected API endpoints and routes
- [x] Add, edit, delete transactions (income/expenses)
- [x] Categorize transactions
- [x] View financial summary (income, expenses, balance)
- [x] Set monthly budgets
- [x] Compare budget vs actual expenses
- [x] Transaction filtering by date, category, amount
- [x] Pagination for transaction list
- [x] Dashboard with D3.js pie chart
- [x] Budget page with D3.js bar chart
- [x] Responsive design
- [x] Modern, clean UI

### Additional Features 
- Real-time budget percentage calculations
- Visual progress bars for budgets
- Color-coded transaction types
- Hover effects and animations
- Mobile-friendly responsive design
- Category-wise summaries
- Over-budget warnings

## User Flow

1. User visits the application and is redirected to the login page
2. User logs in with credentials
3. Dashboard displays financial summary with pie chart
4. User can:
   - View all transactions with filtering and pagination
   - Add new income or expense transactions
   - Edit or delete existing transactions
   - Set monthly budgets
   - View budget comparison with bar chart
5. User can logout when done

##  Project Structure

```
Spendly/
├── backend/
│   ├── budget_tracker/          # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── finances/                # Main Django app
│   │   ├── models.py           # Database models
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   ├── urls.py             # API routes
│   │   ├── filters.py          # Custom filters
│   │   └── admin.py            # Admin configuration
│   ├── manage.py
│   ├── setup_initial_data.py   # Demo data script
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Layout.jsx
│   │   │   ├── TransactionForm.jsx
│   │   │   ├── TransactionList.jsx
│   │   │   ├── TransactionFilters.jsx
│   │   │   ├── BudgetForm.jsx
│   │   │   └── *.css
│   │   ├── pages/              # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Transactions.jsx
│   │   │   ├── Budget.jsx
│   │   │   └── *.css
│   │   ├── context/            # React context
│   │   │   └── AuthContext.jsx
│   │   ├── services/           # API services
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── AI_REQUIREMENTS.md
```

##  Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

##  Deployment

### Backend Deployment (Render/Railway/PythonAnywhere)

1. Set environment variables in hosting platform
2. Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
3. Set `DEBUG=False` for production
4. Use PostgreSQL for production database
5. Run migrations and collect static files

### Frontend Deployment (Vercel/Netlify/GitHub Pages)

1. Update `VITE_API_URL` to point to deployed backend
2. Build the project: `npm run build`
3. Deploy the `dist` folder
4. Configure build settings in hosting platform

##  Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

##  Known Limitations

- SQLite is used for development; PostgreSQL recommended for production
- No email verification or password reset functionality
- Limited to monthly budget periods
- No support for recurring transactions

##  Assumptions Made

1. Users are pre-created (demo user provided for testing)
2. All monetary amounts are in USD
3. Budgets are set on a monthly basis
4. Categories are user-specific
5. Each transaction must be associated with a category
6. Transaction type must match category type

##  Attributions

### Libraries & Frameworks
- **Django**: Backend web framework
- **Django REST Framework**: RESTful API development
- **React**: Frontend UI library
- **Vite**: Frontend build tool
- **D3.js**: Data visualization library
- **Axios**: HTTP client for API requests
- **React Router**: Client-side routing

### AI Assistance
- This project was developed with assistance from AI (Claude by Anthropic)
- AI helped with:
  - Project structure and boilerplate code
  - Component architecture design
  - D3.js chart implementations
  - CSS styling and responsive design
  - README documentation

### Design Inspiration
- Color scheme inspired by modern financial applications
- UI/UX patterns follow industry best practices
- Chart designs based on D3.js documentation examples



---

