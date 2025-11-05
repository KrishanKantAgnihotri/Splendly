from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, date
from decimal import Decimal
from .models import Category, Transaction, Budget
from .serializers import (
    CategorySerializer, TransactionSerializer, BudgetSerializer,
    UserSerializer, FinancialSummarySerializer
)
from .filters import TransactionFilter


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    # Validation
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(password) < 8:
        return Response(
            {'error': 'Password must be at least 8 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Create default categories for new user
        default_categories = [
            ('Salary', 'income'),
            ('Freelance', 'income'),
            ('Investments', 'income'),
            ('Other Income', 'income'),
            ('Groceries', 'expense'),
            ('Rent', 'expense'),
            ('Utilities', 'expense'),
            ('Transportation', 'expense'),
            ('Entertainment', 'expense'),
            ('Healthcare', 'expense'),
            ('Dining Out', 'expense'),
            ('Shopping', 'expense'),
        ]
        
        for name, cat_type in default_categories:
            Category.objects.create(user=user, name=name, type=cat_type)
        
        # Generate token
        token = Token.objects.create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Registration failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint that returns authentication token
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint that deletes authentication token
    """
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Get current authenticated user information
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing categories
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['type']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing transactions with filtering and pagination
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('category')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get financial summary with totals and category breakdowns
        """
        # Get query parameters for date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Base queryset
        queryset = self.get_queryset()
        
        # Apply date filters if provided
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # Calculate totals
        income_total = queryset.filter(type='income').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        expense_total = queryset.filter(type='expense').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        balance = income_total - expense_total
        
        # Expense breakdown by category
        expense_by_category = queryset.filter(type='expense').values(
            'category__name', 'category__id'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        expense_categories = [
            {
                'category': item['category__name'],
                'category_id': item['category__id'],
                'amount': float(item['total'])
            }
            for item in expense_by_category
        ]
        
        # Income breakdown by category
        income_by_category = queryset.filter(type='income').values(
            'category__name', 'category__id'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        income_categories = [
            {
                'category': item['category__name'],
                'category_id': item['category__id'],
                'amount': float(item['total'])
            }
            for item in income_by_category
        ]
        
        # Monthly trend (last 6 months)
        from django.db.models.functions import TruncMonth
        monthly_data = queryset.annotate(
            month=TruncMonth('date')
        ).values('month', 'type').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        # Organize monthly data
        monthly_dict = {}
        for item in monthly_data:
            month_str = item['month'].strftime('%Y-%m')
            if month_str not in monthly_dict:
                monthly_dict[month_str] = {'month': month_str, 'income': 0, 'expense': 0}
            monthly_dict[month_str][item['type']] = float(item['total'])
        
        monthly_trend = list(monthly_dict.values())
        
        summary_data = {
            'total_income': income_total,
            'total_expenses': expense_total,
            'balance': balance,
            'expense_by_category': expense_categories,
            'income_by_category': income_categories,
            'monthly_trend': monthly_trend,
        }
        
        serializer = FinancialSummarySerializer(summary_data)
        return Response(serializer.data)


class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing budgets
    """
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['month', 'year', 'category']
    ordering_fields = ['year', 'month', 'amount']
    ordering = ['-year', '-month']
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related('category')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current_month(self, request):
        """
        Get budget for the current month
        """
        today = date.today()
        budgets = self.get_queryset().filter(month=today.month, year=today.year)
        serializer = self.get_serializer(budgets, many=True)
        return Response(serializer.data)

