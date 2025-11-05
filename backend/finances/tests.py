from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
from .models import Category, Transaction, Budget


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_create_category(self):
        category = Category.objects.create(
            user=self.user,
            name='Test Category',
            type='expense'
        )
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.type, 'expense')
        self.assertEqual(str(category), 'Test Category (expense)')


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(
            user=self.user,
            name='Groceries',
            type='expense'
        )
        
    def test_create_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            type='expense',
            amount=Decimal('50.00'),
            category=self.category,
            date=date.today(),
            description='Test transaction'
        )
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.type, 'expense')


class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_create_budget(self):
        budget = Budget.objects.create(
            user=self.user,
            month=1,
            year=2024,
            amount=Decimal('1000.00')
        )
        self.assertEqual(budget.amount, Decimal('1000.00'))
        self.assertEqual(budget.month, 1)


class AuthenticationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_login_success(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        
    def test_login_invalid_credentials(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
    def test_create_category(self):
        response = self.client.post('/api/categories/', {
            'name': 'Test Category',
            'type': 'expense'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Category')
        
    def test_list_categories(self):
        Category.objects.create(user=self.user, name='Category 1', type='income')
        Category.objects.create(user=self.user, name='Category 2', type='expense')
        
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TransactionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(
            user=self.user,
            name='Test Category',
            type='expense'
        )
        
    def test_create_transaction(self):
        response = self.client.post('/api/transactions/', {
            'type': 'expense',
            'amount': '50.00',
            'category': self.category.id,
            'date': str(date.today()),
            'description': 'Test transaction'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_transactions(self):
        Transaction.objects.create(
            user=self.user,
            type='expense',
            amount=Decimal('50.00'),
            category=self.category,
            date=date.today()
        )
        
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BudgetAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
    def test_create_budget(self):
        response = self.client.post('/api/budgets/', {
            'month': 1,
            'year': 2024,
            'amount': '1000.00'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_current_month_budget(self):
        today = date.today()
        Budget.objects.create(
            user=self.user,
            month=today.month,
            year=today.year,
            amount=Decimal('1000.00')
        )
        
        response = self.client.get('/api/budgets/current_month/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

