from django_filters import rest_framework as filters
from .models import Transaction


class TransactionFilter(filters.FilterSet):
    """
    Custom filter for Transaction model
    Allows filtering by date range, category, amount range, and type
    """
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')
    amount_min = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    category = filters.NumberFilter(field_name='category__id')
    type = filters.ChoiceFilter(choices=Transaction.TRANSACTION_TYPES)
    
    class Meta:
        model = Transaction
        fields = ['date_from', 'date_to', 'amount_min', 'amount_max', 'category', 'type']

