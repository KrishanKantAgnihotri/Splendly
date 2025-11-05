from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Transaction, Budget
from decimal import Decimal


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    user = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def validate(self, data):
        # Ensure the user can't create duplicate categories
        user = self.context['request'].user
        name = data.get('name')
        
        if self.instance:  # Update
            if Category.objects.filter(user=user, name=name).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'name': 'You already have a category with this name.'})
        else:  # Create
            if Category.objects.filter(user=user, name=name).exists():
                raise serializers.ValidationError({'name': 'You already have a category with this name.'})
        
        return data


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    user = serializers.ReadOnlyField(source='user.id')
    category_name = serializers.ReadOnlyField(source='category.name')
    category_type = serializers.ReadOnlyField(source='category.type')
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'type', 'amount', 'category', 'category_name',
            'category_type', 'date', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate(self, data):
        # Ensure category belongs to the user
        user = self.context['request'].user
        category = data.get('category')
        
        if category and category.user != user:
            raise serializers.ValidationError({'category': 'Invalid category selection.'})
        
        # Validate that transaction type matches category type
        transaction_type = data.get('type')
        if category and transaction_type and category.type != transaction_type:
            raise serializers.ValidationError({
                'category': f'Selected category is for {category.type}, but transaction type is {transaction_type}.'
            })
        
        return data


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget model"""
    user = serializers.ReadOnlyField(source='user.id')
    category_name = serializers.ReadOnlyField(source='category.name')
    actual_expenses = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'month', 'year', 'amount', 'category',
            'category_name', 'actual_expenses', 'remaining',
            'percentage_used', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_month(self, value):
        if not 1 <= value <= 12:
            raise serializers.ValidationError("Month must be between 1 and 12.")
        return value
    
    def validate_year(self, value):
        if value < 2000 or value > 2100:
            raise serializers.ValidationError("Year must be between 2000 and 2100.")
        return value
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget amount must be greater than zero.")
        return value
    
    def validate(self, data):
        # Ensure category belongs to the user (if provided)
        user = self.context['request'].user
        category = data.get('category')
        
        if category and category.user != user:
            raise serializers.ValidationError({'category': 'Invalid category selection.'})
        
        # Ensure category is expense type (if provided)
        if category and category.type != 'expense':
            raise serializers.ValidationError({'category': 'Budget can only be set for expense categories.'})
        
        return data
    
    def get_actual_expenses(self, obj):
        """Calculate actual expenses for the budget period"""
        from django.db.models import Sum
        from datetime import date
        
        start_date = date(obj.year, obj.month, 1)
        if obj.month == 12:
            end_date = date(obj.year + 1, 1, 1)
        else:
            end_date = date(obj.year, obj.month + 1, 1)
        
        filters = {
            'user': obj.user,
            'type': 'expense',
            'date__gte': start_date,
            'date__lt': end_date,
        }
        
        if obj.category:
            filters['category'] = obj.category
        
        total = Transaction.objects.filter(**filters).aggregate(total=Sum('amount'))['total']
        return float(total) if total else 0.0
    
    def get_remaining(self, obj):
        """Calculate remaining budget"""
        actual = self.get_actual_expenses(obj)
        return float(obj.amount) - actual
    
    def get_percentage_used(self, obj):
        """Calculate percentage of budget used"""
        actual = self.get_actual_expenses(obj)
        if obj.amount > 0:
            return round((actual / float(obj.amount)) * 100, 2)
        return 0.0


class FinancialSummarySerializer(serializers.Serializer):
    """Serializer for financial summary data"""
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    expense_by_category = serializers.ListField(child=serializers.DictField())
    income_by_category = serializers.ListField(child=serializers.DictField())
    monthly_trend = serializers.ListField(child=serializers.DictField())

