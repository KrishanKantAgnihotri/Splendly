from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Category model for classifying transactions"""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ['name', 'user']
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    """Transaction model for tracking income and expenses"""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.type.capitalize()}: {self.amount} - {self.category.name} ({self.date})"


class Budget(models.Model):
    """Budget model for setting monthly spending limits"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    month = models.IntegerField(validators=[MinValueValidator(1)])  # 1-12
    year = models.IntegerField(validators=[MinValueValidator(2000)])
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='budgets',
        null=True,
        blank=True,
        help_text="Leave blank for overall budget"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['user', 'month', 'year', 'category']
    
    def __str__(self):
        category_str = f" - {self.category.name}" if self.category else " (Overall)"
        return f"Budget {self.year}-{self.month:02d}{category_str}: {self.amount}"

