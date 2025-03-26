import django_filters
from ..models import SellHeader

class SellHeaderFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains', label='Search by Code')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact', label='Search by Date')

    class Meta:
        model = SellHeader
        fields = ['code', 'date']
