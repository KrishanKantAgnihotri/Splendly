from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'user', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'amount', 'category', 'user', 'created_at']
    list_filter = ['type', 'date', 'category', 'created_at']
    search_fields = ['description', 'user__username', 'category__name']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'year', 'amount', 'category', 'created_at']
    list_filter = ['year', 'month', 'created_at']
    search_fields = ['user__username', 'category__name']

