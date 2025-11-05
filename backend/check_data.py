"""
Quick script to check if data exists in database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')
django.setup()

from finances.models import Category, Transaction, Budget
from django.contrib.auth.models import User

print("=" * 50)
print("DATABASE CHECK")
print("=" * 50)

# Check users
users = User.objects.all()
print(f"\nUsers: {users.count()}")
for user in users:
    print(f"  - {user.username}")

# Check categories
categories = Category.objects.all()
print(f"\nCategories: {categories.count()}")
for cat in categories[:5]:
    print(f"  - {cat.name} ({cat.type}) - User: {cat.user.username}")

# Check transactions
transactions = Transaction.objects.all()
print(f"\nTransactions: {transactions.count()}")

# Check budgets
budgets = Budget.objects.all()
print(f"\nBudgets: {budgets.count()}")

print("\n" + "=" * 50)

