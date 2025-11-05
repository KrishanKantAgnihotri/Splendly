#  Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- pip (Python package manager)
- npm (Node package manager)

## Backend Setup (3 minutes)

1. **Navigate to backend folder:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
# Using py command (recommended for Windows)
py -m pip install -r requirements.txt

# OR using pip directly
pip install -r requirements.txt
```

> **Optional:** Use virtual environment for dependency isolation:
> ```bash
> py -m venv venv && venv\Scripts\activate
> ```

3. **Run migrations:**
```bash
py manage.py migrate
```

4. **Create demo data:**
```bash
py setup_initial_data.py
```

This creates:
- Demo user: `demo` / `demo123456`
- Sample categories (Salary, Rent, Groceries, etc.)
- Sample transactions for last 3 months
- Sample budget for current month

5. **Start backend server:**
```bash
py manage.py runserver
```

Backend API will run at: http://localhost:8000/api/

---

## Frontend Setup (3 minutes)

1. **Open new terminal and navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```

Frontend will run at: http://localhost:5173/

---

## Access the Application

1. **Open browser:** http://localhost:5173
2. **Login with demo credentials:**
   - Username: `demo`
   - Password: `demo123456`
3. **Explore features:**
   - Dashboard with financial summary & D3.js pie chart
   - Transactions with filtering & pagination
   - Budget management with D3.js bar chart

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
py manage.py runserver 8001
```

**Database errors:**
```bash
# Delete db.sqlite3 and run migrations again
py manage.py migrate --run-syncdb
py setup_initial_data.py
```

**pip not found:**
```bash
# Use py with -m flag
py -m pip install -r requirements.txt
```

### Frontend Issues

**Port already in use:**
Edit `vite.config.js` and change port:
```javascript
server: {
  port: 5174,  // Change to any available port
}
```

**API connection errors:**
Check that backend is running on port 8000

---

## Testing

**Backend tests:**
```bash
cd backend
py manage.py test
```

**Manual testing:**
- Visit Django admin: http://localhost:8000/admin/
- Create superuser: `py manage.py createsuperuser`
- Explore DRF Browsable API: http://localhost:8000/api/

---

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](backend/DEPLOYMENT.md) for deployment guides
- Customize categories and transactions
- Set your own budgets
- Explore all filtering options

---

## Common Commands

**Backend:**
```bash
# Create superuser
py manage.py createsuperuser

# Run tests
py manage.py test

# Create new migration
py manage.py makemigrations

# Apply migrations
py manage.py migrate

# Collect static files
py manage.py collectstatic
```

**Frontend:**
```bash
# Install packages
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

**🎉 You're all set! Happy budgeting!**

