import django_filters
from ..models import PurchaseHeader

class PurchaseHeaderFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains', label='Search by Code')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact', label='Search by Date')

    class Meta:
        model = PurchaseHeader
        fields = ['code', 'date']
