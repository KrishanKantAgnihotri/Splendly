"""
Script to set up initial data for the application
Creates a demo user with sample categories and transactions
"""
import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from finances.models import Category, Transaction, Budget

def setup_demo_user():
    """Create demo user and sample data"""
    
    # Create demo user
    user, created = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@example.com',
            'first_name': 'Demo',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password('demo123456')
        user.save()
        print("✓ Created demo user (username: demo, password: demo123456)")
    else:
        print("✓ Demo user already exists")
    
    # Create sample categories
    income_categories = [
        'Salary',
        'Freelance',
        'Investments',
        'Other Income'
    ]
    
    expense_categories = [
        'Groceries',
        'Rent',
        'Utilities',
        'Transportation',
        'Entertainment',
        'Healthcare',
        'Dining Out',
        'Shopping',
        'Education',
        'Insurance'
    ]
    
    print("\n✓ Creating categories...")
    for cat_name in income_categories:
        Category.objects.get_or_create(
            user=user,
            name=cat_name,
            type='income'
        )
    
    for cat_name in expense_categories:
        Category.objects.get_or_create(
            user=user,
            name=cat_name,
            type='expense'
        )
    
    print(f"  Created {len(income_categories)} income categories")
    print(f"  Created {len(expense_categories)} expense categories")
    
    # Create sample transactions
    if Transaction.objects.filter(user=user).count() == 0:
        print("\n✓ Creating sample transactions...")
        
        # Get categories
        salary_cat = Category.objects.get(user=user, name='Salary', type='income')
        freelance_cat = Category.objects.get(user=user, name='Freelance', type='income')
        groceries_cat = Category.objects.get(user=user, name='Groceries', type='expense')
        rent_cat = Category.objects.get(user=user, name='Rent', type='expense')
        utilities_cat = Category.objects.get(user=user, name='Utilities', type='expense')
        transport_cat = Category.objects.get(user=user, name='Transportation', type='expense')
        entertainment_cat = Category.objects.get(user=user, name='Entertainment', type='expense')
        dining_cat = Category.objects.get(user=user, name='Dining Out', type='expense')
        
        today = date.today()
        
        # Sample transactions for the last 3 months
        transactions_data = [
            # Current month
            ('income', salary_cat, Decimal('5000.00'), today - timedelta(days=5), 'Monthly salary'),
            ('expense', rent_cat, Decimal('1200.00'), today - timedelta(days=3), 'Monthly rent payment'),
            ('expense', groceries_cat, Decimal('85.50'), today - timedelta(days=2), 'Weekly groceries'),
            ('expense', utilities_cat, Decimal('120.00'), today - timedelta(days=1), 'Electricity and water'),
            ('expense', transport_cat, Decimal('50.00'), today, 'Gas'),
            
            # Last month
            ('income', salary_cat, Decimal('5000.00'), today - timedelta(days=35), 'Monthly salary'),
            ('income', freelance_cat, Decimal('800.00'), today - timedelta(days=32), 'Freelance project'),
            ('expense', rent_cat, Decimal('1200.00'), today - timedelta(days=33), 'Monthly rent'),
            ('expense', groceries_cat, Decimal('250.00'), today - timedelta(days=30), 'Monthly groceries'),
            ('expense', utilities_cat, Decimal('115.00'), today - timedelta(days=28), 'Utilities'),
            ('expense', entertainment_cat, Decimal('60.00'), today - timedelta(days=25), 'Movie tickets'),
            ('expense', dining_cat, Decimal('45.00'), today - timedelta(days=22), 'Restaurant'),
            ('expense', transport_cat, Decimal('80.00'), today - timedelta(days=20), 'Gas and parking'),
            
            # 2 months ago
            ('income', salary_cat, Decimal('5000.00'), today - timedelta(days=65), 'Monthly salary'),
            ('expense', rent_cat, Decimal('1200.00'), today - timedelta(days=63), 'Monthly rent'),
            ('expense', groceries_cat, Decimal('280.00'), today - timedelta(days=60), 'Monthly groceries'),
            ('expense', utilities_cat, Decimal('125.00'), today - timedelta(days=58), 'Utilities'),
            ('expense', entertainment_cat, Decimal('75.00'), today - timedelta(days=55), 'Concert tickets'),
            ('expense', dining_cat, Decimal('120.00'), today - timedelta(days=52), 'Dinner with friends'),
            ('expense', transport_cat, Decimal('90.00'), today - timedelta(days=50), 'Gas'),
        ]
        
        for trans_type, category, amount, trans_date, description in transactions_data:
            Transaction.objects.create(
                user=user,
                type=trans_type,
                category=category,
                amount=amount,
                date=trans_date,
                description=description
            )
        
        print(f"  Created {len(transactions_data)} sample transactions")
    else:
        print("\n✓ Sample transactions already exist")
    
    # Create sample budget
    current_month = date.today().month
    current_year = date.today().year
    
    if not Budget.objects.filter(user=user, month=current_month, year=current_year, category__isnull=True).exists():
        print("\n✓ Creating sample budget...")
        Budget.objects.create(
            user=user,
            month=current_month,
            year=current_year,
            amount=Decimal('3000.00'),
            category=None  # Overall budget
        )
        print("  Created overall monthly budget of $3000")
    else:
        print("\n✓ Sample budget already exists")
    
    print("\n" + "="*50)
    print("Setup complete!")
    print("="*50)
    print("\nDemo Account Credentials:")
    print("  Username: demo")
    print("  Password: demo123456")
    print("\n" + "="*50)

if __name__ == '__main__':
    setup_demo_user()

